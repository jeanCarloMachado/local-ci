#!/usr/bin/env python


from grimoire.ask_question import AskQuestion
import os
branch = AskQuestion().ask("Give the branch name")
os.system(f"git fetch ; git checkout {branch}")