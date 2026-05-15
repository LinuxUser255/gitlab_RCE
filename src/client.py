"""Shared HTTP session and GitLab API helpers used by every exploit."""

from __future__ import annotations

import random
import string
import sys

import requests
import urllib3

from .parsers import GitlabParse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GitlabClient:
    """HTTP session and shared helpers for interacting with a GitLab instance.

    All exploit modules receive an instance of this class rather than
    inheriting from a common base, keeping composition over inheritance.
    """

    DEFAULT_PORT: int = 42069
    DEFAULT_EMAIL_DOMAIN: str = "laboratory.htb"

    def __init__(self, url: str, local_ip: str) -> None:
        self.url = url
        self.local_ip = local_ip
        self.port = self.DEFAULT_PORT
        # Override if the target restricts registration to a specific domain.
        self.email_domain = self.DEFAULT_EMAIL_DOMAIN
        self.session = requests.Session()
        self.username: str = ""
        self.password: str = ""
        # Informational — exploits should prefer the return value of
        # create_empty_project() over indexing into this list.
        self.projects: list[str] = []
        self.issues: list[str] = []

    # ------------------------------------------------------------------ #
    # Utilities                                                          #
    # ------------------------------------------------------------------ #

    def randomize(self) -> str:
        """Return a random 10-character alphanumeric string."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=10))

    def abort(self) -> None:
        print("Something went wrong! ABORT MISSION!")
        sys.exit(1)

    # ------------------------------------------------------------------ #
    # CSRF token                                                         #
    # ------------------------------------------------------------------ #

    def get_authenticity_token(self, url: str, i: int = -1) -> str:
        result = self.session.get(url, verify=False)
        token = GitlabParse().feed(result.text, i)
        if not token:
            print("could not get token!")
            self.abort()
        return token  # type: ignore[return-value]  # abort() exits on None

    # ------------------------------------------------------------------ #
    # User lifecycle                                                     #
    # ------------------------------------------------------------------ #

    def register_user(self) -> None:
        token = self.get_authenticity_token(self.url + "/users/sign_in")
        self.username = self.randomize()
        self.password = self.randomize()
        data = {
            "new_user[email]": f"{self.username}@{self.email_domain}",
            "new_user[email_confirmation]": f"{self.username}@{self.email_domain}",
            "new_user[username]": self.username,
            "new_user[name]": self.username,
            "new_user[password]": self.password,
            "authenticity_token": token,
        }
        result = self.session.post(self.url + "/users", data=data, verify=False)
        print(
            f"registering {self.username}:{self.password}"
            f" - {result.status_code}"
        )

    def login_user(self) -> None:
        token = self.get_authenticity_token(self.url + "/users/sign_in", 0)
        data = {
            "authenticity_token": token,
            "user[login]": self.username,
            "user[password]": self.password,
        }
        result = self.session.post(
            self.url + "/users/sign_in", data=data, verify=False
        )
        print(result.status_code)

    def delete_user(self) -> None:
        token = self.get_authenticity_token(self.url + "/profile/account")
        data = {
            "authenticity_token": token,
            "_method": "delete",
            "password": self.password,
        }
        result = self.session.post(self.url + "/users", data=data, verify=False)
        print(f"delete user {self.username} - {result.status_code}")

    # ------------------------------------------------------------------ #
    # Project / issue management                                         #
    # ------------------------------------------------------------------ #

    def create_empty_project(self) -> str:
        """Create a new private project and return its name."""
        token = self.get_authenticity_token(self.url + "/projects/new")
        project = self.randomize()
        self.projects.append(project)
        data = {
            "authenticity_token": token,
            "project[ci_cd_only]": "false",
            "project[name]": project,
            "project[path]": project,
            "project[visibility_level]": "0",
            "project[description]": "all your base are belong to us",
        }
        result = self.session.post(
            self.url + "/projects", data=data, verify=False
        )
        print(f"creating project {project} - {result.status_code}")
        return project

    def create_issue(self, project_id: str, text: str) -> None:
        issue_link = f"{self.url}/{self.username}/{project_id}/issues"
        token = self.get_authenticity_token(issue_link + "/new")
        issue_title = self.randomize()
        self.issues.append(issue_title)
        data = {
            "authenticity_token": token,
            "issue[title]": issue_title,
            "issue[description]": text,
        }
        result = self.session.post(issue_link, data=data, verify=False)
        print(
            f"creating issue {issue_title} for project {project_id}"
            f" - {result.status_code}"
        )
