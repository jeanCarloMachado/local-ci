#!/usr/bin/env python3

import os


class AutoChecks:
    def fix(self):
        os.system("black . ")
        os.system("isort . ")
        self.tests()

    def tests(self):
        if not os.path.exists("tests"):
            print("There is no tests folder so will skip the tests")
            return

        self._run("pytest", fail_on_error=True)

    def _run(self, cmd, fail_on_error=True):
        result = os.system(cmd)
        if result != 0 and fail_on_error:
            raise Exception(f"Comand: {cmd} failed")


if __name__ == "__main__":
    import fire

    fire.Fire(AutoChecks)
