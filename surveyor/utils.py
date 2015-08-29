# -*- coding: utf-8 -*-


from __future__ import unicode_literals


def strtobool(val):
    if not val:
        return False

    strval = str(val).strip().lower()
    if strval in ("1", "y", "yes", "true", "on"):
        return True
    if strval in ("0", "n", "no", "false", "off"):
        return False

    raise ValueError(val)


def guess_text(text):
    text = text.strip()

    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text
