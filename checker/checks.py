"""Sanity checks for a Helm values file of a data platform on Kubernetes.

Checks are generic: every component that defines resources should set
requests and limits, replica counts should be sensible, and secrets should
not be committed in plain text.
"""
import re

SECRET_KEY = re.compile(r"(password|secret|token|apikey|api_key)", re.I)


def walk(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, node


def check(values):
    issues = []
    stack = [("", values)]
    while stack:
        path, node = stack.pop()
        if isinstance(node, dict):
            res = node.get("resources")
            if isinstance(res, dict):
                for kind in ("requests", "limits"):
                    if not res.get(kind):
                        issues.append((path or "root", f"resources.{kind} is missing"))
            for k, v in node.items():
                stack.append((f"{path}.{k}" if path else k, v))
    for p, v in walk(values):
        leaf = p.split(".")[-1]
        if SECRET_KEY.search(leaf) and isinstance(v, str) and v and not v.startswith("$"):
            issues.append((p, "possible plain-text secret, use a Kubernetes Secret"))
    for p, v in walk(values):
        if p.endswith("replicas") and v == 0:
            issues.append((p, "replicas is 0"))
    return issues
