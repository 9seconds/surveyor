# -*- coding: utf-8 -*-


from __future__ import unicode_literals


class SurveyorError(Exception):
    pass


class XMLParseError(SurveyorError, ValueError):
    pass


class UnexpectedTagError(XMLParseError):

    def __init__(self, incoming, expected):
        message = "Expected tag is {0}, but got {1}".format(expected, incoming)
        super(UnexpectedTagError, self).__init__(message)


class CannotImportClassError(XMLParseError):

    def __init__(self, classpath, exception):
        message = "Cannot import '{0}': {1}".format(classpath, exception)
        super(CannotImportClassError, self).__init__(message)


class CannotFindElementClass(XMLParseError):

    def __init__(self, class_module, class_name):
        message = "Cannot find '{0}' in module '{1.__name__}' ({1.__file__})".format(class_name, class_module)
        super(CannotFindElementClass, self).__init__(message)
