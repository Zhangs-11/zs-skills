import ipaddress
import unittest
from unittest.mock import MagicMock, patch
from urllib.parse import urlsplit

import wechat_publisher.secure_download as secure_download


class SecureDownloadTests(unittest.TestCase):
    def test_status_check_uses_head_and_follows_only_revalidated_redirects(self) -> None:
        first_response = MagicMock()
        first_response.status = 302
        first_response.getheader.return_value = "https://docs.example.com/final"
        second_response = MagicMock()
        second_response.status = 200
        second_response.getheader.return_value = None
        first_connection = MagicMock()
        first_connection.getresponse.return_value = first_response
        second_connection = MagicMock()
        second_connection.getresponse.return_value = second_response
        first_parsed = urlsplit("https://example.com/start")
        second_parsed = urlsplit("https://docs.example.com/final")
        address = ipaddress.ip_address("93.184.216.34")

        with (
            patch.object(
                secure_download,
                "_validated_target",
                side_effect=[(first_parsed, [address]), (second_parsed, [address])],
            ) as validate,
            patch.object(
                secure_download,
                "_connection_for",
                side_effect=[first_connection, second_connection],
            ),
        ):
            status = secure_download.check_public_url_status(first_parsed.geturl())

        self.assertEqual(status, 200)
        self.assertEqual(validate.call_count, 2)
        self.assertEqual(first_connection.request.call_args.args[0], "HEAD")

    def test_status_check_rejects_private_literal_without_connecting(self) -> None:
        with patch.object(secure_download, "_connection_for") as connection_for:
            with self.assertRaisesRegex(secure_download.SecureDownloadError, "private or local"):
                secure_download.check_public_url_status("http://127.0.0.1/delete?id=1")

        connection_for.assert_not_called()

    def test_download_connects_to_the_prevalidated_ip(self) -> None:
        response = MagicMock()
        response.status = 200
        response.getheader.side_effect = lambda name, default=None: {
            "content-type": "image/png",
            "content-length": "3",
        }.get(name, default)
        response.read.side_effect = [b"png", b""]
        connection = MagicMock()
        connection.getresponse.return_value = response
        parsed = urlsplit("https://images.example.com/picture.png")
        address = ipaddress.ip_address("93.184.216.34")

        with (
            patch.object(
                secure_download,
                "_validated_target",
                return_value=(parsed, [address]),
            ),
            patch.object(
                secure_download,
                "_connection_for",
                return_value=connection,
            ) as connection_for,
        ):
            result = secure_download.download_public_url(
                parsed.geturl(),
                max_bytes=10,
                supported_content_types={"image/png"},
            )

        connection_for.assert_called_once_with(parsed, str(address), 30)
        self.assertEqual(result.body, b"png")
        connection.request.assert_called_once()

    def test_private_literal_address_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            secure_download.SecureDownloadError,
            "private or local",
        ):
            secure_download.download_public_url(
                "http://127.0.0.1/image.png",
                max_bytes=10,
            )

    def test_non_global_shared_and_site_local_addresses_are_rejected(self) -> None:
        for url in (
            "http://100.64.0.1/image.png",
            "http://[fec0::1]/image.png",
        ):
            with self.subTest(url=url):
                with self.assertRaisesRegex(
                    secure_download.SecureDownloadError,
                    "private or local",
                ):
                    secure_download.download_public_url(url, max_bytes=10)

    def test_https_can_be_required(self) -> None:
        with self.assertRaisesRegex(
            secure_download.SecureDownloadError,
            "must use HTTPS",
        ):
            secure_download.download_public_url(
                "http://93.184.216.34/image.png",
                max_bytes=10,
                require_https=True,
            )


if __name__ == "__main__":
    unittest.main()
