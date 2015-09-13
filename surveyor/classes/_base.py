# -*- coding: utf-8 -*-


from __future__ import unicode_literals, absolute_import

import abc

import six

from six.moves import range


@six.add_metaclass(abc.ABCMeta)
class Style(object):

    @abc.abstractmethod
    def stylize(self):
        raise NotImplementedError("One has to implement stylize method!")


class CellStyle(Style):

    def __init__(self, cell):
        self.cell = cell

    def stylize(self):
        pass


class RowStyle(Style):

    def __init__(self, cells):
        self.cells = cells

    def __iter__(self):
        return iter(self.cells)

    def stylize(self):
        pass


class TableStyle(Style):

    def __init__(self, sheet, top_row, bottom_row, left_column, right_column):
        self.sheet = sheet
        self.top_row = top_row
        self.bottom_row = bottom_row
        self.left_column = left_column
        self.right_column = right_column

    def __iter__(self):
        for row_idx in range(self.top_row, self.bottom_row + 1):
            yield [
                self.sheet.cell(row=row_idx, column=col_idx)
                for col_idx in range(self.left_column, self.right_column + 1)
            ]

    def stylize(self):
        pass


class SheetStyle(Style):

    def __init__(self, sheet):
        self.sheet = sheet

    def stylize(self):
        pass
