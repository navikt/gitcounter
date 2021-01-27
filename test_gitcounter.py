import gitcounter
import os
import shutil

repo_dir = "test/test_repo"


def build_test_repo():
    deep_path = repo_dir + "/terraform/teams/team_test/apps"
    os.makedirs(deep_path, exist_ok=True)
    shutil.copyfile("test/resources/testapp.yml", deep_path + "/testapp.yaml")

def test_count_databases():
    build_test_repo()
    gc = gitcounter.GitCounter(repo_dir=repo_dir)

    counters = gc.count_databases()

    assert counters["postgres"] == 1
    assert counters["oracle"] == 1

    shutil.rmtree(repo_dir)
