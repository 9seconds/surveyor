# -*- coding: utf-8 -*-


import pytest

import surveyor.utils as utils


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize("value", (
    "1",
    "y",
    "yes",
    "true",
    "True",
    "Yes",
    "YES",
    "TRUE",
    "ON",
    "on"
))
def test_strtobool_true(value):
    assert utils.strtobool(value)


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize("value", (
    "0",
    "n",
    "no",
    "false",
    "False",
    "FALSE",
    "Off",
    "off",
    "NO",
    "N",
    None
))
def test_strtobool_false(value):
    assert not utils.strtobool(value)


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize("value", (
    [1],
    {1: 1},
))
def test_strtobool_unknown(value):
    with pytest.raises(ValueError):
        utils.strtobool(value)


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize("value, result", (
    ("1", 1),
    ("-1", -1),
    ("0", 0),
    ("0.1", 0.1),
    ("-0.1", -0.1),
    (".1", 0.1),
    ("1.", 1.0),
    ("", ""),
    ("text", "text"),
    ("1text", "1text"),
    ("2 text", "2 text"),
    ("1.0 text", "1.0 text")
))
def test_guess_text_int(value, result):
    assert utils.guess_text(value) == result
