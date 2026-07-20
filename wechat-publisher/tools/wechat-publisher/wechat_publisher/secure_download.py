from __future__ import annotations

import http.client
import ipaddress
import socket
from dataclasses import dataclass
from urllib.parse import SplitResult, urlsplit, urlunsplit


class SecureDownloadError(RuntimeError):
    pass


@dataclass(frozen=True)
class DownloadedContent:
    body: bytes
    content_type: str


class _PinnedHTTPConnection(http.client.HTTPConnection):
    def __init__(self, host: str, port: int, pinned_ip: str, timeout: float) -> None:
        super().__init__(host, port=port, timeout=timeout)
        self._pinned_ip = pinned_ip

    def connect(self) -> None:
        self.sock = socket.create_connection(
            (self._pinned_ip, self.port),
            self.timeout,
            self.source_address,
        )


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host: str, port: int, pinned_ip: str, timeout: float) -> None:
        super().__init__(host, port=port, timeout=timeout)
        self._pinned_ip = pinned_ip

    def connect(self) -> None:
        sock = socket.create_connection(
            (self._pinned_ip, self.port),
            self.timeout,
            self.source_address,
        )
        # 连接固定到已验证 IP，但 SNI/证书仍校验原始域名。
        self.sock = self._context.wrap_socket(sock, server_hostname=self.host)


def download_public_url(
    url: str,
    *,
    max_bytes: int,
    supported_content_types: set[str] | None = None,
    timeout: float = 30,
    require_https: bool = False,
) -> DownloadedContent:
    parsed, addresses = _validated_target(url, require_https=require_https)
    last_error: Exception | None = None
    for address in addresses:
        connection = _connection_for(parsed, str(address), timeout)
        try:
            target = urlunsplit(("", "", parsed.path or "/", parsed.query, ""))
            connection.request(
                "GET",
                target,
                headers={"Host": parsed.netloc, "User-Agent": "wechat-publisher/0.1"},
            )
            response = connection.getresponse()
            if 300 <= response.status < 400:
                raise SecureDownloadError("remote image redirects are not allowed")
            if response.status >= 400:
                raise SecureDownloadError(
                    f"remote image returned HTTP {response.status}"
                )
            content_type = response.getheader("content-type", "")
            normalized = content_type.split(";", 1)[0].strip().lower()
            if supported_content_types is not None and normalized not in supported_content_types:
                raise SecureDownloadError(
                    f"unsupported remote image content type: {content_type or 'missing'}"
                )
            content_length = _content_length(response.getheader("content-length"))
            if content_length is not None and content_length > max_bytes:
                raise SecureDownloadError("remote image is too large")
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = response.read(min(64 * 1024, max_bytes + 1 - total))
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise SecureDownloadError("remote image is too large")
                chunks.append(chunk)
            return DownloadedContent(b"".join(chunks), normalized)
        except SecureDownloadError:
            raise
        except (OSError, http.client.HTTPException) as exc:
            last_error = exc
        finally:
            connection.close()
    raise SecureDownloadError("remote image connection failed") from last_error


def _validated_target(
    url: str,
    *,
    require_https: bool = False,
) -> tuple[SplitResult, list[ipaddress.IPv4Address | ipaddress.IPv6Address]]:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise SecureDownloadError("remote image URL must use HTTP or HTTPS")
    if require_https and parsed.scheme != "https":
        raise SecureDownloadError("remote image URL must use HTTPS")
    try:
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
    except ValueError as exc:
        raise SecureDownloadError("remote image URL contains an invalid port") from exc
    expected_port = 443 if parsed.scheme == "https" else 80
    if port != expected_port:
        raise SecureDownloadError("remote image uses an unsupported port")
    hostname = parsed.hostname.rstrip(".").lower()
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise SecureDownloadError("remote image points to a private or local address")
    try:
        addresses = [ipaddress.ip_address(hostname)]
    except ValueError:
        try:
            addresses = list(
                dict.fromkeys(
                    ipaddress.ip_address(item[4][0])
                    for item in socket.getaddrinfo(
                        hostname,
                        port,
                        type=socket.SOCK_STREAM,
                    )
                )
            )
        except socket.gaierror as exc:
            raise SecureDownloadError(
                f"remote image host cannot be resolved: {hostname}"
            ) from exc
    if not addresses or any(not _is_public(address) for address in addresses):
        raise SecureDownloadError("remote image points to a private or local address")
    return parsed, addresses


def _connection_for(
    parsed: SplitResult,
    pinned_ip: str,
    timeout: float,
) -> http.client.HTTPConnection:
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    if parsed.scheme == "https":
        return _PinnedHTTPSConnection(host, port, pinned_ip, timeout)
    return _PinnedHTTPConnection(host, port, pinned_ip, timeout)


def _content_length(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        length = int(value)
    except ValueError as exc:
        raise SecureDownloadError("invalid remote image content length") from exc
    if length < 0:
        raise SecureDownloadError("invalid remote image content length")
    return length


def _is_public(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    return bool(
        address.is_global
        and not address.is_multicast
        and not getattr(address, "is_site_local", False)
    )
