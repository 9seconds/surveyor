# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
import os.path
import shutil

import magic

import surveyor


XLSX_MIME_TYPES = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel"
)
"""MIME type for XLSX."""


def test_main(request, tmpdir, monkeypatch):
    xml = """
    <?xml version="1.0" encoding="UTF-8"?>
    <workbook>
        <sheet>
            <table>
                <tr>
                    <td>Name</td>
                    <td>Value</td>
                </tr>
                <tr>
                    <td>1</td>
                    <td>2text</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>4.0</td>
                </tr>
            </table>
            <table startcell="C10">
                <tr>
                    <td>Book</td>
                    <td>Title</td>
                </tr>
                <tr>
                    <td>111</td>
                    <td>222text</td>
                </tr>
                <tr>
                    <td>333</td>
                    <td>444.0</td>
                </tr>
            </table>
        </sheet>
        <sheet>
            <table>
                <tr>
                    <td>Book</td>
                    <td>Title</td>
                </tr>
                <tr>
                    <td>111</td>
                    <td>222text</td>
                </tr>
                <tr>
                    <td>333</td>
                    <td>444.0</td>
                </tr>
            </table>
        </sheet>
    </workbook>
    """.strip()

    request.addfinalizer(lambda: shutil.rmtree(tmpdir.strpath))

    template_path = tmpdir.join("template.xml").strpath
    with open(template_path, "wt") as res:
        # noinspection PyTypeChecker
        res.write(xml)

    output_path = tmpdir.join("output.xlsx").strpath

    monkeypatch.setattr("sys.argv", ["surveyor", "-o", output_path, template_path])

    assert surveyor.main() == os.EX_OK
    assert os.path.exists(output_path)
    assert magic.from_file(output_path, mime=True).decode("utf-8") in XLSX_MIME_TYPES
