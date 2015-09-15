# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import pytest

import surveyor.parse as parse


def test_check_sheet_names():
    xml = """
    <workbook>
        <sheet name="Worksheet1" />
        <sheet autosize="true" />
        <sheet />
        <sheet name="Custom" />
    </workbook>
    """.strip()

    workbook = parse.parse_fileobj(xml)
    workbook = workbook.process()

    assert workbook.worksheets[0].title == "Worksheet1"
    assert workbook.worksheets[1].title == "Sheet2"
    assert workbook.worksheets[2].title == "Sheet3"
    assert workbook.worksheets[3].title == "Custom"


def test_fill_table():
    xml = """
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

    workbook = parse.parse_fileobj(xml)
    workbook = workbook.process()

    assert workbook.worksheets[0].cell(row=1, column=1).value == "Name"
    assert workbook.worksheets[0].cell(row=1, column=2).value == "Value"
    assert workbook.worksheets[0].cell(row=2, column=1).value == 1
    assert workbook.worksheets[0].cell(row=2, column=2).value == "2text"
    assert workbook.worksheets[0].cell(row=3, column=1).value == 3
    assert workbook.worksheets[0].cell(row=3, column=2).value == 4.0

    assert workbook.worksheets[0].cell(row=10, column=3).value == "Book"
    assert workbook.worksheets[0].cell(row=10, column=4).value == "Title"
    assert workbook.worksheets[0].cell(row=11, column=3).value == 111
    assert workbook.worksheets[0].cell(row=11, column=4).value == "222text"
    assert workbook.worksheets[0].cell(row=12, column=3).value == 333
    assert workbook.worksheets[0].cell(row=12, column=4).value == 444.0

    assert workbook.worksheets[1].cell(row=1, column=1).value == "Book"
    assert workbook.worksheets[1].cell(row=1, column=2).value == "Title"
    assert workbook.worksheets[1].cell(row=2, column=1).value == 111
    assert workbook.worksheets[1].cell(row=2, column=2).value == "222text"
    assert workbook.worksheets[1].cell(row=3, column=1).value == 333
    assert workbook.worksheets[1].cell(row=3, column=2).value == 444.0


@pytest.mark.parametrize("number_format", (
    "0",
    "0.00",
    "#,##0",
    "#,##0.00"
))
def test_check_inline_number_format(number_format):
    xml = """
    <workbook>
        <sheet>
            <table>
                <tr>
                    <td number_format="{0}">1</td>
                </tr>
            </table>
        </sheet>
    </workbook>
    """.format(number_format).strip()

    workbook = parse.parse_fileobj(xml)
    workbook = workbook.process()

    assert workbook.worksheets[0].cell(row=1, column=1).number_format == number_format
