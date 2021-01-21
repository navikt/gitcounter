import gitcounter as gc
import os
import shutil


repo_path = "test/test_repo"


def build_test_repo():
    deep_path = repo_path + "/terraform/teams/team_test/apps"
    os.makedirs(deep_path, exist_ok=True)
    shutil.copyfile("test/resources/testapp.yml", deep_path + "/testapp.yaml")


def test_build_repo():
    assert not os.path.exists(repo_path)
    build_test_repo()
    assert os.path.exists(repo_path)
    gc.delete_repo(repo_path)
    assert not os.path.exists(repo_path)


