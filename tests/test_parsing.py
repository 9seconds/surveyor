# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import pytest

import surveyor.exceptions as exceptions
import surveyor.parse as parse


# noinspection PyUnresolvedReferences
def test_incorrect_root():
    xml = """
    <root></root>
    """.strip()

    with pytest.raises(exceptions.UnexpectedTagError):
        parse.parse_fileobj(xml)


# noinspection PyUnresolvedReferences
def test_workbook_no_classes():
    xml = """
    <workbook classes="asiodfsdfhdjflksghdlfkg.dfghsdkjfghdskfgds.gdfg" />
    """.strip()

    with pytest.raises(exceptions.CannotImportClassError):
        parse.parse_fileobj(xml)


def test_workbook_default_classes():
    xml = """
    <workbook />
    """.strip()

    workbook = parse.parse_fileobj(xml)

    assert workbook.classes.__name__ == "surveyor.classes.simple"


def test_workbook_set_classes():
    xml = """
    <workbook classes="surveyor.classes.simple" />
    """.strip()

    workbook = parse.parse_fileobj(xml)

    assert workbook.classes.__name__ == "surveyor.classes.simple"


def test_found_sheets():
    xml = """
    <workbook>
        <sheet />
        <sheet />
        <sheet />
        <sheet />
    </workbook>
    """.strip()

    workbook = parse.parse_fileobj(xml)

    assert len(workbook.children) == 4


def test_sheet_set_names():
    xml = """
    <workbook>
        <sheet name="Worksheet1" />
        <sheet />
        <sheet />
        <sheet name="Custom" />
    </workbook>
    """.strip()

    workbook = parse.parse_fileobj(xml)

    assert workbook.children[0].name == "Worksheet1"
    assert workbook.children[1].name == "Sheet2"
    assert workbook.children[2].name == "Sheet3"
    assert workbook.children[3].name == "Custom"


def test_sheet_autosize_setting_default():
    xml = """
    <workbook>
        <sheet />
    </workbook>
    """.strip()

    workbook = parse.parse_fileobj(xml)

    assert not workbook.children[0].autosize


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize("value", (
    "y",
    "yes",
    "on",
    "1",
    "true"
))
def test_sheet_autosize_setting_true(value):
    xml = """
    <workbook>
        <sheet autosize="{0}" />
    </workbook>
    """.format(value).strip()

    workbook = parse.parse_fileobj(xml)

    assert workbook.children[0].autosize


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize("value", (
    "n",
    "no",
    "off",
    "0",
    "false"
))
def test_sheet_autosize_setting_false(value):
    xml = """
    <workbook>
        <sheet autosize="{0}" />
    </workbook>
    """.format(value).strip()

    workbook = parse.parse_fileobj(xml)

    assert not workbook.children[0].autosize


def test_sheet_class():
    xml = """
    <workbook>
        <sheet class="Test" />
        <sheet class="Test2" />
    </workbook>
    """.strip()

    workbook = parse.parse_fileobj(xml)

    assert workbook.children[0].klass == "Test"
    assert workbook.children[1].klass == "Test2"


def test_found_tables():
    xml = """
    <workbook>
        <sheet>
            <table class="Test11" />
            <table class="Test12" />
        </sheet>
        <sheet>
            <table class="Test21" />
            <table class="Test22" />
        </sheet>
    </workbook>
    """.strip()

    workbook = parse.parse_fileobj(xml)

    assert len(workbook.children[0].children) == 2
    assert workbook.children[0].children[0].klass == "Test11"
    assert workbook.children[0].children[1].klass == "Test12"

    assert len(workbook.children[1].children) == 2
    assert workbook.children[1].children[0].klass == "Test21"
    assert workbook.children[1].children[1].klass == "Test22"


def test_table_start_cell():
    xml = """
    <workbook>
        <sheet>
            <table startcell="A5" />
        </sheet>
    </workbook>
    """.strip()

    workbook = parse.parse_fileobj(xml)

    assert workbook.children[0].children[0].start_cell == "A5"


def test_table_default_start_cell():
    xml = """
    <workbook>
        <sheet>
            <table />
        </sheet>
    </workbook>
    """.strip()

    workbook = parse.parse_fileobj(xml)

    assert workbook.children[0].children[0].start_cell == "A1"


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize("column", (
    "C",
    3
))
def test_table_start_cell_numbered(column):
    xml = """
    <workbook>
        <sheet>
            <table startrow="10" startcolumn="{0}" />
        </sheet>
    </workbook>
    """.format(column).strip()

    workbook = parse.parse_fileobj(xml)

    assert workbook.children[0].children[0].start_cell == "C10"


def test_row_class():
    xml = """
    <workbook>
        <sheet>
            <table>
                <tr class="Classname" />
            </table>
        </sheet>
    </workbook>
    """.strip()

    workbook = parse.parse_fileobj(xml)

    assert workbook.children[0].children[0].children[0].klass == "Classname"


def test_cell_class():
    xml = """
    <workbook>
        <sheet>
            <table>
                <tr>
                    <td class="Classname"></td>
                </tr>
            </table>
        </sheet>
    </workbook>
    """.strip()

    workbook = parse.parse_fileobj(xml)

    assert workbook.children[0].children[0].children[0].children[0].klass == "Classname"


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize("text, result", (
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
def test_cell_text_guessing(text, result):
    xml = """
    <workbook>
        <sheet>
            <table>
                <tr>
                    <td class="Classname">{0}</td>
                </tr>
            </table>
        </sheet>
    </workbook>
    """.format(text).strip()

    workbook = parse.parse_fileobj(xml)

    assert workbook.children[0].children[0].children[0].children[0].value == result
