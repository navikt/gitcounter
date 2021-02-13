#!/usr/bin/python3

# Std-lib imports
import logging
import os
import pathlib

# Third-party imports
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import yaml


class GitCounter:
    def __init__(self, repo_dir="./"):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.repo_dir = repo_dir
        self.prometheus_url = "http://nais-prometheus-pushgateway.nais:9091"

    def run(self):
        self.logger.info("Creating registry...")
        registry = CollectorRegistry()
        gauge = Gauge("databases_onprem", "number of databases onprem (from vault-iac)", ["type"], registry=registry)
        counters = self.count_proddatabases()
        self.logger.info(counters)
        for key, value in counters.items():
            gauge.labels(key).set(value)

        push_to_gateway(self.prometheus_url, job='gitcounter', registry=registry)
        self.logger.info("Pushed to gateway!")

    def count_proddatabases(self):

        oracle, postgres = 0, 0
        for path in self.get_app_yamls(self.repo_dir):
            data = yaml.load(
                pathlib.Path(path).read_text(),
                Loader=yaml.CLoader,
            )
            for k, v in data["clusters"].items():
                if not k.startswith("prod"): continue
                for ki, vi in v.items():
                    if ki == "oracle": oracle += 1
                    if ki == "postgresql": postgres += 1

        return {
            "oracle": oracle,
            "postgres": postgres
        }

    def get_app_yamls(self, rootdir):
        yield from (
            path
            for path
            in pathlib.Path(rootdir).glob(f"**/apps/**/*.*")
            if path.is_file()
        )


if __name__ == "__main__":
    m = GitCounter()
    m.run()
