#!/usr/bin/env python3
import logging
import os
import sys

import fire

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])


class CommitChangeAssistant:
    """
    A tool to commit to git while using precommit
    """

    DEFAULT_COMMIT_MESSAGE = "Automatic commit"

    def __init__(self):
        print("Start commit assistant")
        self.commit_message = CommitChangeAssistant.DEFAULT_COMMIT_MESSAGE

    def start(self, commit_message=None, disable_add=False):
        """
        Executes the entire commit procedure with a push in the end
        """

        self.disable_add = disable_add

        if not os.path.exists(".pre-commit-config.yaml"):
            logging.warning("No pre-commit configuration found, consider adding one")

        result = self.commit_and_retry(commit_message)
        if result:
            self.push_and_log()

    def commit(self, commit_message=None, see_diff=True):
        self.commit_message = commit_message

        import subprocess

        has_diff = subprocess.getoutput("git status --porcelain")
        if not has_diff:
            logging.info("No changes to commit. Exiting early.")
            sys.exit(0)

        if see_diff:
            self._see_all_diff()

        if not self.commit_message:
            self.commit_message = input("Give a commit message: ")
            if not self.commit_message:
                self.commit_message = CommitChangeAssistant.DEFAULT_COMMIT_MESSAGE

        result = os.system(f"auto_checks.py fix")
        if result != 0:
            return False

        if not self.disable_add:
            os.system("git add .")
        os.system(f"git add . ")
        result = os.system(f"git commit -m '{self.commit_message}'")

        if result != 0:
            raise Exception("The commit failed")

    def commit_and_retry(self, commit_message=None) -> bool:
        try:
            result = self.commit(commit_message)
        except Exception as e:
            return self._manage_error()

        return result

    def push_and_log(self):
        command = "git push origin $(current_branch.sh)"
        os.system(command)
        os.system("git log")

    def _manage_error(self) -> bool:
        message = f"""Current commit message: {self.commit_message}
Failed [t] try again, [s] skip verify, commit & push [v] view diff: """
        given_input = input(message)
        if given_input == "t":
            return self.commit_and_retry(self.commit_message)
        elif given_input == "s":
            os.system(f"git commit -m '{self.commit_message}' --no-verify ")
            self.push_and_log()
        elif given_input == "v":
            self._see_all_diff()
            self._manage_error()
        else:
            self._manage_error()

        return False

    def _see_all_diff(self):
        """Shows the entire git diff staged and unstaged"""
        os.system(f"git status -vv")

    def _see_uncached_diff(self):
        """SHows the entire git diff staged and unstaged"""
        os.system(f"git diff")

    def _see_cached_diff(self):
        """Display only the already staged difference"""
        os.system(f"git diff --cached")


if __name__ == "__main__":
    fire.Fire(CommitChangeAssistant)
