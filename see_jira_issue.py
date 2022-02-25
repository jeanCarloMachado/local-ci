#!/usr/bin/env python


from grimoire.ask_question import AskQuestion
import os
issue= AskQuestion().ask("Give the issue id")
os.system(f"$BROWSER https://getyourguide.atlassian.net/browse/{issue}")