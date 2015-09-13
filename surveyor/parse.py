# -*- coding: utf-8 -*-


from __future__ import unicode_literals, absolute_import

try:
    import lxml.etree as etree
except ImportError:
    try:
        # noinspection PyPep8Naming
        import xml.etree.cElementTree as etree
    except ImportError:
        # noinspection PyPep8Naming
        import xml.etree.ElementTree as etree

import surveyor.elements
import surveyor.exceptions


def parse_filename(filename):
    with open(filename, "r") as resource:
        return parse_fileobj(resource)


def parse_fileobj(content):
    root = etree.parse(content)
    root = root.getroot()
    parsed = parse_xml(root)

    return parsed


def parse_xml(root):
    workbook = surveyor.elements.WorkBook(root)

    for sheet_element in root.findall(surveyor.elements.Sheet.TAG_NAME):
        sheet = surveyor.elements.Sheet(sheet_element)
        workbook.add(sheet)

        for table_element in sheet_element.findall(surveyor.elements.Table.TAG_NAME):
            table = surveyor.elements.Table(table_element)
            sheet.add(table)

            for row_element in table_element.findall(surveyor.elements.Row.TAG_NAME):
                row = surveyor.elements.Row(row_element)
                table.add(row)

                for cell_element in row_element.findall(surveyor.elements.Cell.TAG_NAME):
                    cell = surveyor.elements.Cell(cell_element)
                    row.add(cell)

    return workbook
