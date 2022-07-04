#!/usr/bin/env python3

import os


class AutoChecks:
    """
    Perform automated checks and fixes for any project that you uses
    """

    def fix(self):
        self.fast()

    def fast(self):
        os.system("black . ")
        os.system("isort . ")
        self.builds()
        self.tests()

    def secrets(self):
        os.system("tell-me-your-secrets .")

    def builds(self):
        # makes sure that the code can be compiled
        self._fail_on_error("pylint tests --disable=all --enable=E0401 tests")

    def slow(self):
        self.fast()
        os.system("mypy . ")
        self.secrets()

    def tests(self):
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
