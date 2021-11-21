from PyQt5 import QtGui
import csv


def format(colour, is_bold, is_italic):
    """
    The function joins setting of colour, bold and italic to one QTextCharFormat
    :param colour: (str) HEX-format colour (example: #ff00ff)
    :param is_bold: (bool) if True QColor will be bold else QColor won't
    :param is_italic: (bool) if True QColor will be italic else QColor won't
    :return: (QTextCharFormat)
    """
    _color = QtGui.QColor()
    _color.setNamedColor(colour)

    _format = QtGui.QTextCharFormat()
    _format.setForeground(_color)
    if is_bold:
        _format.setFontWeight(QtGui.QFont.Bold)
    if is_italic:
        _format.setFontItalic(True)

    return _format


def reading_csv_linter(name_of_file):
    """
    The function reads csv table with styles for linter and make of it table
    :param name_of_file: (str) name of csv table
    :return: (list) massive of dicts with setting of linter
    """
    with open(file=name_of_file) as csvfile:
        design = csv.DictReader(csvfile, delimiter=';', quotechar='"')

        return list(design)


def making_styles(data_):
    """
    Create dict where keys are element of linter and
    values are settings of elements
    :param data_: (list) massive of dicts of csv table
    :return: (dict) dict of QTextCharFormat
    """
    STYLES = dict()
    for dct in data_:
        is_bold = True if dct['bold'] == 'True' else False
        is_italic = True if dct['italic'] == 'True' else False
        STYLES[dct['name']] = format(dct['HEX-colour'], is_bold, is_italic)
    return STYLES


def all_together(name):
    """
    The function joins two function in one to be called in another module
    :param name: name of csv table with linter settings
    :return: (dict) dict of QTextCharFormat
    """
    return making_styles(reading_csv_linter(name))


if __name__ == '__main__':
    data = reading_csv_linter('linter_csv_table.csv')
    print(making_styles(data))
