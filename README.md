# Helm Values Checker

A tiny linter for Helm values files of Kubernetes-based data platforms. It flags missing resource requests and limits, zero replicas and plain-text secrets, and exits non-zero so it can run in CI.

```bash
pip install -r requirements.txt
python -m checker examples/values.yaml
```

Tests: pytest.
