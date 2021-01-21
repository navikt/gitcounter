#!/usr/bin/python3

from prometheus_client import start_http_server, Gauge
import logging
from git import Repo
import time
import shutil


class GitCounter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.git_url = "https://github.com/navikt/vault-iac"
        self.repo_dir = "vault-iac"
        self.timeout = 60
        self.sleep =  300

    def run(self):
        self.logger.info("starting metrics http server on port 8000")
        start_http_server(8000)
        while True:

            #self.clone_GitRepo()
            #self.count_Databases()

            time.sleep(self.sleep)

    def count_databases(self):
        logging.info("counting databases")
        postgres = Gauge("databases_postgres", "number of postgres databases", ['team'])

        postgres.set(30)


def clone_repo(git_url, repo_dir):
    logging.info("cloning repo")
    Repo.clone_from(git_url, repo_dir)


def delete_repo(repo_dir):
    logging.info("deleting repo")
    shutil.rmtree(repo_dir)


if __name__ == "__main__":
    m = GitCounter()
    m.run()
