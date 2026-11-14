from checker.checks import check


def test_detects_issues():
    v = {"a": {"replicas": 0, "resources": {"requests": {"cpu": 1}}},
         "db": {"adminPassword": "x"}}
    msgs = [m for _, m in check(v)]
    assert any("limits" in m for m in msgs)
    assert any("replicas is 0" in m for m in msgs)
    assert any("secret" in m for m in msgs)


def test_clean():
    v = {"a": {"replicas": 2, "resources": {"requests": {"cpu": 1}, "limits": {"cpu": 1}}}}
    assert check(v) == []
