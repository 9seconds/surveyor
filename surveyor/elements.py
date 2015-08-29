# -*- coding: utf-8 -*-


from __future__ import unicode_literals, absolute_import

import abc
import collections
import importlib

import openpyxl
import openpyxl.utils
import six

import surveyor.exceptions
import surveyor.utils

from six.moves import range, zip


DEFAULT_CLASSES_MODULE = "surveyor.classes.simple"
"""Default importable module with style classes."""


@six.add_metaclass(abc.ABCMeta)
class BaseElement(object):

    TAG_NAME = None

    @property
    def classes(self):
        return self.parent.classes

    def __init__(self, element):
        if element.tag.lower() != self.TAG_NAME:
            raise surveyor.exceptions.UnexpectedTagError(element.tag, self.TAG_NAME)

        super(BaseElement, self).__init__()

        self.parent = None
        self.klass = None
        self.children = []

    def add(self, element):
        element.parent = self
        self.children.append(element)

    @abc.abstractmethod
    def process(self, element=None):
        raise NotImplementedError("You have to implement this method before invoke it.")

    def get_class(self, name):
        class_obj = getattr(self.classes, name, None)
        if class_obj is None:
            raise surveyor.exceptions.CannotFindElementClass(self.classes, name)

        return class_obj


class WorkBook(BaseElement):

    TAG_NAME = "workbook"

    ATTR_CLASSES = "classes"

    @property
    def classes(self):
        return self.class_module

    def __init__(self, element):
        super(WorkBook, self).__init__(element)

        module_name = self.make_module_name(element)

        try:
            self.class_module = importlib.import_module(module_name)
        except Exception as exc:
            raise surveyor.exceptions.CannotImportClassError(module_name, exc)

    def add(self, element):
        super(WorkBook, self).add(element)

        if not element.name:
            element.name = "Sheet{0}".format(len(self.children))

    def process(self, element=None):
        book = openpyxl.Workbook(encoding="utf-8", guess_types=True)
        book.worksheets = []

        for sheet in self.children:
            sheet_element = book.create_sheet(title=sheet.name)
            sheet.process(sheet_element)

        return book

    def make_module_name(self, element):
        return element.attrib.get(self.ATTR_CLASSES, DEFAULT_CLASSES_MODULE)


class Sheet(BaseElement):

    TAG_NAME = "sheet"

    ATTR_AUTOSIZE = "autosize"
    ATTR_NAME = "name"

    DEFAULT_WIDTH = 10
    WIDTH_ADDITION = 1

    def __init__(self, element):
        super(Sheet, self).__init__(element)

        self.autosize = surveyor.utils.strtobool(element.attrib.get(self.ATTR_AUTOSIZE))
        self.name = element.attrib.get(self.ATTR_NAME)

    def process(self, element=None):
        for table in self.children:
            table.process(element)

        if self.autosize:
            self.apply_autosize(element)

    def apply_autosize(self, sheet, default_width=DEFAULT_WIDTH, width_addition=WIDTH_ADDITION):
        column_width = collections.defaultdict(lambda: default_width)

        for row in range(1, sheet.max_row):
            for col in range(1, sheet.max_column + 1):
                value = sheet.cell(row=row, column=col).value
                if value:
                    if not isinstance(value, basestring):
                        value = str(value)
                    # Skip formulas
                    if value.startswith("="):
                        continue
                    column_width[col] = max(column_width[col], len(value))

        for col in range(1, sheet.max_column + 1):
            column = sheet.column_dimensions[openpyxl.utils.get_column_letter(col)]
            column.auto_size = True
            column.width = column_width[col] + width_addition


class Table(BaseElement):

    TAG_NAME = "table"

    ATTR_START_CELL = "startcell"
    ATTR_START_ROW = "startrow"
    ATTR_START_COLUMN = "startcolumn"
    ATTR_CLASS = "class"

    DEFAULT_START_CELL = "A1"

    @classmethod
    def get_start_cell(cls, attrs):
        start_row = attrs[cls.ATTR_START_ROW]
        start_column = attrs[cls.ATTR_START_COLUMN]

        if start_column.isdigit():
            start_column = openpyxl.utils.get_column_letter(int(start_column))
        start_column = start_column.upper()

        return start_column + start_row

    def __init__(self, element):
        super(Table, self).__init__(element)

        self.klass = element.attrib.get(self.ATTR_CLASS)
        if self.ATTR_START_CELL in element.attrib:
            self.start_cell = element.attrib[self.ATTR_START_CELL]
        elif self.ATTR_START_ROW in element.attrib and self.ATTR_START_COLUMN in element.attrib:
            self.start_cell = self.get_start_cell(element.attrib)
        else:
            self.start_cell = self.DEFAULT_START_CELL

    def process(self, element=None):
        top_row, bottom_row, left_column, right_column = self.get_dimensions()

        for row, row_idx in zip(self.children, range(top_row, bottom_row)):
            row.process(element, row_idx, left_column, right_column)

    def get_dimensions(self):
        left_column, top_row = openpyxl.utils.coordinate_from_string(self.start_cell)
        left_column = openpyxl.utils.column_index_from_string(left_column)

        bottom_row = top_row + len(self.children)
        right_column = left_column + max(len(row.children) for row in self.children)

        return top_row, bottom_row, left_column, right_column


class Row(BaseElement):

    TAG_NAME = "tr"

    ATTR_CLASS = "class"

    def __init__(self, element):
        super(Row, self).__init__(element)

        self.klass = element.attrib.get(self.ATTR_CLASS)

    def process(self, element=None, row_idx=1, left_column=1, right_column=1):
        for col_idx, cell in enumerate(self.children, start=left_column):
            cell.process(element, row_idx, col_idx)


class Cell(BaseElement):

    TAG_NAME = "td"

    ATTR_CLASS = "class"

    def __init__(self, element):
        super(Cell, self).__init__(element)

        self.klass = element.attrib.get(self.ATTR_CLASS)
        self.value = surveyor.utils.guess_text(element.text)

    def process(self, element=None, row_idx=1, col_idx=1):
        cell = element.cell(row=row_idx, column=col_idx)
        cell.value = self.value
