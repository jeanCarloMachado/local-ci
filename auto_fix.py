#!/usr/bin/env python3

import os


class AutoFix:
    def fix(self):
        os.system("black . ")
        os.system("isort . ")


if __name__ == "__main__":
    import fire

    fire.Fire(AutoFix)
