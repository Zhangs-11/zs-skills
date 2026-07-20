import ipaddress
import unittest
from unittest.mock import MagicMock, patch
from urllib.parse import urlsplit

import wechat_publisher.secure_download as secure_download


class SecureDownloadTests(unittest.TestCase):
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
