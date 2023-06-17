import os


def test_envs_available():
    port = os.environ.get("PORT")
    assert port is not None
