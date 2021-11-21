from dialog_design_interface import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtCore
import sys
from readingcsvdesign import reading_csv_design
import os

real_path = os.getcwd()
if real_path.split(os.sep)[-1] == 'design':
    real_path = os.sep.join(real_path.split(os.sep)[:-1])


class WidgetChangeDesign(QWidget, Ui_Form):
    """The Widget which asks from user about design of Program"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_design.setAlignment(QtCore.Qt.AlignCenter)
        self.update_design()
        self.content_combo()

        self.button_group.buttonClicked.connect(self.was_choice)

    def update_design(self):
        """
        The method defines design of this widget from special csv table design
        :return: None
        """
        design = reading_csv_design(real_path + f'{os.sep}widget_change_design_csv_table.csv')

        for item, value in design.items():
            if item != 'window':
                try:
                    eval(f'self.{item}.setStyleSheet(\'{value}\')')
                except AttributeError:
                    print('No such attribute', item, sep=' ')
            else:
                self.setStyleSheet(value)

    def content_combo(self):
        """
        The method defines comboBox of all possible designs
        :return:
        """
        pos_designs = os.listdir(real_path + f'{os.sep}design_tables')
        self.all_designs_combo.addItems(pos_designs)

    def was_choice(self, button=None):
        """
        The method processes user's choice
        :param button:
        :return:
        """
        if button.text() == self.ok_button.text():
            changing_csv_tables(self.all_designs_combo.currentText())
            self.update_design()

        self.close()
        return None


def changing_csv_tables(name_of_design):
    """
    The function copies csv tables from storage to work csv tables
    :param name_of_design: name of folder where design is kept
    :return: None
    """
    os.chdir(real_path + f'{os.sep}design_tables{os.sep}{name_of_design}')

    with open(file='design_csv_table.csv', mode='r') as file:
        main_design = file.read()

    with open(file='linter_csv_table.csv', mode='r') as file:
        linter_design = file.read()

    with open(file='widget_change_design_csv_table.csv', mode='r') as file:
        widget_design = file.read()

    os.chdir(real_path)

    with open(file='design_csv_table.csv', mode='w') as file:
        file.write(main_design)

    with open(file='linter_csv_table.csv', mode='w') as file:
        file.write(linter_design)

    with open(file='widget_change_design_csv_table.csv', mode='w') as file:
        file.write(widget_design)

    return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WidgetChangeDesign()
    ex.show()
    sys.exit(app.exec())
