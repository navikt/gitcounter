#!/usr/bin/python3

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import logging
import os
import pandas as pd


class GitCounter:
    def __init__(self,  repo_dir="./"):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.repo_dir = repo_dir
        self.timeout = 60
        self.sleep = 3600
        self.prometheus_url = "http://nais-prometheus-pushgateway.nais:9091"

    def run(self):
        self.logger.info("Creating registry...")
        registry = CollectorRegistry()
        gauges = {"postgres": Gauge("databases_postgres", "number of postgres databases"),
                  "oracle": Gauge("databases_oracle", "number of oracle databases")}

        counters = self.count_databases()

        self.logger.info(counters)
        for key, value in counters.items():
            gauges[key].set(value)
            gauges[key].set_to_current_time()

        push_to_gateway(self.prometheus_url, job='gitcounter', registry=registry)
        self.logger.info("Pushed to gateway!")

    def count_databases(self):
        self.logger.info("counting databases")

        app_yamls = self.get_app_yamls(self.repo_dir)

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
