# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
import os.path
import optparse

import surveyor.parse


__version__ = 0, 1, 0
"""Package version."""

DEFAULT_FILENAME = "result.xlsx"
"""Default filename to save."""

DEFAULT_FILEPATH = os.path.join(os.getcwd(), DEFAULT_FILENAME)
"""Default filepath to save into."""


def get_options():
    usage = "%prog [-o OUTPUT_FILEPATH] TEMPLATE_FILEPATH"

    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-o", "--output",
                      help="Filepath to store result file. Default is '{0}'".format(DEFAULT_FILEPATH),
                      metavar="OUTPUT_FILEPATH",
                      default=DEFAULT_FILEPATH)

    parsed, args = parser.parse_args()
    if len(args) == 0:
        parser.error("Mandatory TEMPLATE_FILEPATH has to be set.")

    return parsed.output, args[0]


def main():
    out_filename, template_filename = get_options()
    parsed = surveyor.parse.parse_filename(template_filename)
    workbook = parsed.process()
    workbook.save(out_filename)

    return os.EX_OK
