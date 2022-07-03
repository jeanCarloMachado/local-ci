#!/usr/bin/env python3
import os

import fire
from grimoire.ask_question import AskQuestion


class Cli:
    def ask(self):
        branch = AskQuestion().ask("Give the branch name")
        self.change(branch)

    def change(self, branch):
        os.system(f"git fetch ; git checkout {branch}")


if __name__ == "__main__":
    fire.Fire(Cli)
