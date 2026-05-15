"""HTML parsers for scraping GitLab response pages."""

from __future__ import annotations

from html.parser import HTMLParser


class GitlabParse(HTMLParser):
    """Parse CSRF/authenticity tokens from GitLab forms and meta tags."""

    def __init__(self) -> None:
        super().__init__()
        self.tokens: list[str] = []
        self.current_name: str = ""

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == "input":
            for name, value in attrs:
                if (
                    self.current_name == "authenticity_token"
                    and name == "value"
                ):
                    self.tokens.append(value)
                self.current_name = value
        elif tag == "meta":
            for name, value in attrs:
                if self.current_name == "csrf-token":
                    self.tokens.append(value)
                self.current_name = value

    def feed(self, data: str, i: int = -1) -> str | None:  # type: ignore[override]
        super().feed(data)
        try:
            return self.tokens[i]
        except IndexError:
            return None


class ProjectIDParse(HTMLParser):
    """Parse the hidden project_id input from a GitLab project page."""

    def __init__(self) -> None:
        super().__init__()
        self.project_found: bool = False
        self.project_id: int | None = None

    def feed(self, data: str) -> int | None:  # type: ignore[override]
        super().feed(data)
        return self.project_id

    def handle_starttag(self, tag: str, attrs: list) -> None:
        for name, value in attrs:
            if self.project_found and name == "value":
                self.project_id = int(value)
                return
            self.project_found = name == "id" and value == "project_id"


class VersionParse(HTMLParser):
    """Parse the GitLab version string from the /help page."""

    def __init__(self) -> None:
        super().__init__()
        self.found_version: bool = False
        self.version: str | None = None

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == "a":
            for name, value in attrs:
                self.found_version = name == "href" and "/tags/v" in value

    def handle_data(self, data: str) -> None:
        if self.found_version and not self.version:
            self.version = data

    def feed(self, data: str) -> str | None:  # type: ignore[override]
        super().feed(data)
        return self.version
