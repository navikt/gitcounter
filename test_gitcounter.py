import gitcounter
import os
import shutil

repo_dir = "test/test_repo"


def build_test_repo():
    os.makedirs(repo_dir + "/terraform/teams/team_test/apps", exist_ok=True)
    os.makedirs(repo_dir + "/terraform/teams/team_test2/apps", exist_ok=True)
    shutil.copyfile("test/resources/apps/testapp.yml", repo_dir + "/terraform/teams/team_test/apps" + "/testapp.yaml")
    shutil.copyfile("test/resources/apps/testapp2.yml", repo_dir + "/terraform/teams/team_test/apps" + "/testapp2.yaml")
    shutil.copyfile("test/resources/apps/testapp3.yml",
                    repo_dir + "/terraform/teams/team_test2/apps" + "/testapp3.yaml")


def test_get_app_yamls():
    build_test_repo()
    gc = gitcounter.GitCounter(repo_dir=repo_dir)
    yamls = gc.get_app_yamls(repo_dir)
    assert len(yamls) == 3
    shutil.rmtree(repo_dir)


def test_count_databases():
    build_test_repo()
    gc = gitcounter.GitCounter(repo_dir=repo_dir)

    counters = gc.count_proddatabases()

    assert counters["postgres"] == 1
    assert counters["oracle"] == 2

    shutil.rmtree(repo_dir)
