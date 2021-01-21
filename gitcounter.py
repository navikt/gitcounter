#!/usr/bin/python3

from prometheus_client import start_http_server, Gauge
import logging
from git import Repo
import time



class GitCounter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.git_url = ""
        self.repo_dir = ""
        self.timeout = 60
        self.sleep =  300

    def run(self):
        self.logger.info("starting metrics http server on port 8000")
        start_http_server(8000)
        while True:

            self.clone_GitRepo()
            self.count_Databases()

        time.sleep(self.sleep)

    def count_Databases(self):
        logging.info("counting databases")
        postgres = Gauge("databases_postgres", "number of postgres databases", ['team'])

        postgres.set(30)

    def clone_GitRepo(self):
        logging.info("cloning repo")
        Repo.clone_from(self.git_url, self.repo_dir)


if __name__ == "__main__":
    m = GitCounter()
    m.run()
