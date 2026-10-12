from ipaddress import ip_address
from urllib.parse import urlparse
import socket


def is_safe_url(url: str) -> bool:
    try:
        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            return False

        if not parsed.hostname:
            return False

        hostname = parsed.hostname.lower()

        if hostname in {"localhost", "localhost.localdomain"}:
            return False

        try:
            ip = ip_address(hostname)

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
                or ip.is_multicast
            ):
                return False

            return True

        except ValueError:
            pass

        try:
            resolved_ips = socket.getaddrinfo(
                hostname,
                None,
                type=socket.SOCK_STREAM,
            )

            for result in resolved_ips:
                resolved_ip = result[4][0]
                ip = ip_address(resolved_ip)

                if (
                    ip.is_private
                    or ip.is_loopback
                    or ip.is_link_local
                    or ip.is_reserved
                    or ip.is_multicast
                ):
                    return False

        except (socket.gaierror, ValueError):
            return False

        return True

    except ValueError:
        return False