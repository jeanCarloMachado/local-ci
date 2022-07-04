#!/usr/bin/env python3

import os


class AutoChecks:
    """
    Perform automated checks and fixes for any project that you uses
    """

    def is_python_project(self):
        return 0 == os.system("[[ $(find . -name '*.py' | wc -l  ) -gt 0 ]]")

    def fix(self):
        self.fast()

    def fast(self):
        self.black()
        self.isort()
        self.assert_python_builds()
        self.tests()
        self.markdown_linter()

    def black(self):
        if not self.is_python_project():
            return

        os.system("black . ")

    def isort(self):
        if not self.is_python_project():
            return

        os.system("isort . ")

    def markdown_linter(self):
        os.system("markdownlint --fix .")

    def secrets(self):
        os.system("tell-me-your-secrets .")

    def assert_python_builds(self):
        # makes sure that the code can be compiled
        self._fail_on_error("pylint tests --disable=all --enable=E0401 tests")

    def slow(self):
        self.fast()
        os.system("mypy . ")
        self.secrets()

    def tests(self):
        if self.is_python_project():
            return

        if not os.path.exists("tests"):
            print("There is no tests folder so will skip the tests")
            return
        self._fail_on_error("pytest")

    def _fail_on_error(self, cmd):
        result = os.system(cmd)
        if result != 0:
            raise Exception(f"Comand: {cmd} failed")


if __name__ == "__main__":
    import fire

    fire.Fire(AutoChecks)
