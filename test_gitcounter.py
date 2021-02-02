import gitcounter
import os
import shutil

repo_dir = "test/test_repo"


def build_test_repo():
    deep_path = repo_dir + "/terraform/teams/team_test/apps"
    os.makedirs(deep_path, exist_ok=True)
    shutil.copyfile("test/resources/apps/testapp.yml", deep_path + "/testapp.yaml")
    shutil.copyfile("test/resources/apps/testapp2.yml", deep_path + "/testapp2.yaml")
    shutil.copyfile("test/resources/apps/testapp3.yml", deep_path + "/testapp3.yaml")

def test_count_databases():
    build_test_repo()
    gc = gitcounter.GitCounter(repo_dir=repo_dir)

    counters = gc.count_proddatabases()

    assert counters["postgres"] == 1
    assert counters["oracle"] == 2

    shutil.rmtree(repo_dir)
