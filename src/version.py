"""Version detection for a GitLab instance."""

from __future__ import annotations

from .client import GitlabClient
from .parsers import VersionParse


def detect_version(client: GitlabClient) -> str | None:
    """Return the GitLab version string, or None if it cannot be parsed.

    Checks reachability first, then scrapes the /help page.
    The caller is responsible for the user lifecycle (register/delete)
    if authentication is needed to view /help.
    """
    try:
        result = client.session.get(client.url, verify=False)
        if result.status_code not in [200, 302]:
            raise RuntimeError(f"Host {client.url} seems down")
    except Exception as exc:
        print(exc)
        client.abort()

    result = client.session.get(client.url + "/help", verify=False)
    print(f"Getting version of {client.url} - {result.status_code}")
    return VersionParse().feed(result.text)
