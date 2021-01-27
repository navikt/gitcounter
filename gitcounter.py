#!/usr/bin/python3

from prometheus_client import start_http_server, Gauge
import logging
from git import Repo
import time
import shutil
import os
import pandas as pd
import re


class GitCounter:
    def __init__(self, git_url="https://github.com/navikt/vault-iac", repo_dir="/github/workspace/"):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.git_url = git_url
        self.repo_dir = repo_dir
        self.timeout = 60
        self.sleep = 3600

    def run(self):
        self.logger.info("starting metrics http server on port 8000")
        start_http_server(8000)
        gauges = {"postgres": Gauge("databases_postgres", "number of postgres databases"),
                  "oracle": Gauge("databases_oracle", "number of oracle databases")}

        while True:
            counters = self.count_databases()

            self.logger.info(counters)
            for key, value in counters.items():
                gauges[key].set(value)

            time.sleep(self.sleep)

    def count_databases(self):
        self.logger.info("counting databases")

        app_yamls = self.get_app_yamls(self.repo_dir + 'test/resources')

        df = pd.DataFrame(app_yamls)
        df.columns = ['path']

        return {
            "oracle": df.apply(lambda x: self.has_oracle(x['path']), axis=1).sum(),
            "postgres": df.apply(lambda x: self.has_pg(x['path']), axis=1).sum()
        }

    def get_app_yamls(self, rootdir):
        app_yamls = []
        for subdir, folders, files in os.walk(rootdir):
            for file in files:
                path = os.path.join(subdir, file)
                if '/apps/' in path:
                    app_yamls.append(path)
        return app_yamls

    def has_oracle(self, path):
        file = open(path).read()
        if 'oracle' in file:
            return 1
        return 0

    def has_pg(self, path):
        file = open(path).read()
        if 'postgresql' in file:
            return 1
        return 0


if __name__ == "__main__":
    m = GitCounter()
    m.run()
