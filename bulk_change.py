#!/usr/bin/env python3
import os

from changes_configs.remove_latest_images import config


class BulkChange:
    def __init__(self, config):
        self.config = config

    def perform_all(self):
        for repo in self.config["repos"]:
            self.perform(repo)

    def perform(self, repo):
        repo_name = repo.split("/")[1]
        print(f"Performing for repo: {repo_name}")
        repo_folder = self._projects_folder() + "/" + repo_name

        self.perform_change(repo)
        self.commit_and_pr(repo)

    def perform_change(self, repo):
        repo_name = repo.split("/")[1]
        print(f"Performing for repo: {repo_name}")
        repo_folder = self._projects_folder() + "/" + repo_name
        self.clone(repo)
        self.reset_changes(repo_folder)
        self.checkout_branch(repo_folder)
        self.change(repo_folder)

    def commit_and_pr(self, repo):
        repo_name = repo.split("/")[1]
        print(f"Performing for repo: {repo_name}")
        repo_folder = self._projects_folder() + "/" + repo_name

        self.commit(repo_folder)
        self.create_pr(repo_name)

    def change(self, repo_folder):
        os.system(f"cd {repo_folder} ; {self.config['shell_change']}")

    def clone(self, repo):
        repo_name = repo.split("/")[1]
        repo_folder = self._projects_folder() + "/" + repo_name
        if os.path.exists(repo_folder):
            print(f"Repo {repo_name} exists not clonning")
            return

        clone_str = f"git@github.com:{repo}.git"
        os.system(f"cd {self._projects_folder()} ; git clone {clone_str}")

    def _projects_folder(self):
        projects_folder = os.environ["HOME"] + "/projects"
        return projects_folder

    def checkout_branch(self, repo_folder):
        os.system(f"cd {repo_folder} && git checkout -b {self.config['branch_name']}")

    def commit(self, repo_folder):
        os.system(
            f"cd {repo_folder} && git add . && git commit -m '{self.config['commit_message']}' "
        )

    def reset_changes(self, repo_folder):
        os.system(
            f"cd {repo_folder} && (git checkout master || git checkout main) && git fetch && git reset --hard HEAD && git clean -f -d"
        )

    def create_pr(self, repo_name):
        repo_folder = self._projects_folder() + "/" + repo_name
        import subprocess

        output = subprocess.getoutput(
            f"cd {repo_folder} &&  run_function current_branch"
        )

        if output != self.config["branch_name"]:
            raise Exception(
                f"Not in the right branch. Current: {output}, while should: {self.config['branch_name']}"
            )

        os.system(
            f"cd {repo_folder} && git add . && gh pr create --fill --body '{self.config['pr_message']}' "
        )


if __name__ == "__main__":
    import fire

    fire.Fire(BulkChange(config))
