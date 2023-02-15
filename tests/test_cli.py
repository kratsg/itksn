from __future__ import annotations

import shlex
import time

import itksn


def test_version(script_runner):
    command = "itksn --version"
    start = time.time()
    ret = script_runner.run(*shlex.split(command))
    end = time.time()
    elapsed = end - start
    assert ret.success
    assert itksn.__version__ in ret.stdout
    assert ret.stderr == ""
    # make sure it took less than a second
    assert elapsed < 1.0


def test_parse(script_runner):
    command = "itksn parse 20Uxxyynnnnnnn"
    ret = script_runner.run(*shlex.split(command))
    assert ret.success
