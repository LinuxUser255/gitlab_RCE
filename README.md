# GitLab RCE / LFI

## Complete refactor code base

Functionality is broken up into modules for easy customization and separation of concerns

Exploit toolkit for old GitLab versions. Primarily seen in CTFs — unlikely to
work against patched production instances. **Educational use only.**



## Affected versions

| Type | Versions |
|------|----------|
| RCE (Redis SSRF) | <= 11.4.7 |
| LFI + RCE (cookie deserialization) | 12.4.0 – 12.8.1 |
| LFI only | 10.4 – 12.8.1 |

## CVEs

- [CVE-2018-19571](https://nvd.nist.gov/vuln/detail/CVE-2018-19571) — SSRF
- [CVE-2018-19585](https://nvd.nist.gov/vuln/detail/CVE-2018-19585) — CRLF injection
- [CVE-2020-10977](https://nvd.nist.gov/vuln/detail/CVE-2020-10977) — path traversal / LFI
- [CVE-2020-8163](https://nvd.nist.gov/vuln/detail/CVE-2020-8163) — RCE via ERB cookie deserialization

## Usage

```bash
pip install -r requirements.txt
chmod +x main.py
./main.py <http://gitlab:port> <local-ip>
```

You will be prompted to select an exploit and start a listener before delivery.

## Credits

- [LiveOverflow](https://www.youtube.com/watch?v=LrLJuyAdoAg)
- [jas502n](https://github.com/jas502n/gitlab-SSRF-redis-RCE)
- [vakzz — HackerOne #827052](https://hackerone.com/reports/827052)
- Partly inspired by the GitLab RCE Metasploit module
