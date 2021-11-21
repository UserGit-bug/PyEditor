import sys
import os

from PyQt5.QtCore import QDir, Qt, QEvent
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QFileSystemModel
from PyQt5.QtGui import QTextCursor, QIcon


from interface import Ui_MainWindow

from readingcsvdesign import reading_csv_design

from dialog_design_program import WidgetChangeDesign

real_path = os.getcwd()
if real_path.split(os.sep)[-1] == 'design':
    real_path = os.sep.join(real_path.split(os.sep)[:-1])

sys.path.append(real_path + f'{os.sep}textwork')
from codework import PythonHighlighter


class Program(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.main_layout.setEnabled(True)

        # Making a title of program
        self.setWindowTitle('PyEditor')

        # Create filemenu in menubar
        self.create_filemenu()

        # Create editmenu in menubar
        self.create_editmenu()

        # Connect design to the window
        self.update_design()

        # Connect icon to the window
        self.setWindowIcon(QIcon('icon.png'))

        # Connect PythonHighlighter for self.editor
        self.highlight = PythonHighlighter(self.editor.document())

        # Setting of some elements in window
        self.editor.installEventFilter(self)
        self.list_with_files.doubleClicked.connect(self.open_the_file_from_list)

    def create_filemenu(self):
        """
        The function create file menu at menubar in the program
        :return: None
        """
        self.filemenu = self.menubar.addMenu('&File')

        # Creating button, which opens new directory and put it in self.list_with_files
        new_project_action = QAction('Open new project', self)
        new_project_action.setStatusTip('Define a path to the directory with your project')
        new_project_action.triggered.connect(lambda: self.question_filepath(None))

        self.filemenu.addAction(new_project_action)

        # Creating button, which opens new exact file and put it in self.editor
        new_file_action = QAction('Open new file', self)
        new_file_action.setStatusTip('Define an exact file to open in the window')
        new_file_action.triggered.connect(lambda: self.question_file(None))

        self.filemenu.addAction(new_file_action)

        # Creating button, which saves file as new file
        new_save_action = QAction('Save as', self)
        new_save_action.setStatusTip('Save file as new file')
        new_save_action.triggered.connect(self.save_as_file)

        self.filemenu.addAction(new_save_action)

        # Creating button, which saves changes in existed file
        save_action = QAction('Save', self)
        save_action.setStatusTip('Save changes in existed file')
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.simply_save_file)

        self.filemenu.addAction(save_action)

        # Creating button, which chang design of our program
        change_design_action = QAction('Change colour scheme', self)
        change_design_action.setStatusTip('Change colour scheme in window')
        change_design_action.triggered.connect(self.action_change_design_trigered)

        self.filemenu.addAction(change_design_action)

    def create_editmenu(self):
        """
        The function create edit menu at menubar in the program
        :return: None
        """
        self.editmenu = self.menubar.addMenu('&Edit')

        # Creating button to copy last line
        copy_line_action = QAction('Copy last line', self)
        copy_line_action.setStatusTip('Copy last line and paste it to the code')
        copy_line_action.setShortcut('Ctrl+D')
        copy_line_action.triggered.connect(self.copy_last_line)

        self.editmenu.addAction(copy_line_action)

    def question_filepath(self, dir_name=None):
        """
        Define path to directory to put it in self.list_with_file (QTreeView)
        :param dir_name: If dir_name is None, user defines a path. Else, dir_name is a path
        :return: None
        """
        if dir_name is None:
            self.dir_name = QFileDialog.getExistingDirectory(self, 'Choose directory', '.')
        else:
            self.dir_name = dir_name

        self.model = QFileSystemModel()
        self.model.setRootPath(self.dir_name)
        self.model.setFilter(QDir.AllDirs | QDir.Hidden | QDir.Files | QDir.NoDotAndDotDot)

        self.list_with_files.setModel(self.model)
        self.list_with_files.setRootIndex(self.model.index(self.dir_name))

    def question_file(self, name_of_file=None):
        """
        Define path to exact file to put it in self.editor (QPlainTextEdit)
        :param name_of_file: If name_of_file is None,
        user defines a path. Else, name_of_file is a path
        :return: None
        """
        if name_of_file is None:
            self.fname = QFileDialog.getOpenFileName(self, 'Choose file', '.',
                                                     'Text docs (*.txt);;Python files (*.py)' +
                                                     ';;All files (*)')[0]
        else:
            self.fname = name_of_file

        try:
            with open(file=self.fname, mode='r', encoding='utf-8') as file:
                self.editor.setPlainText(''.join(file.readlines()))
                self.setWindowTitle(self.fname[self.fname.rfind('/') + 1:])
                self.question_filepath(dir_name=self.fname[:self.fname.rfind('/') + 1])
        except FileNotFoundError:
            pass

    def open_the_file_from_list(self, index):
        """
        Method opens file from self.list_with_files
        """
        try:
            with open(file=self.dir_name + os.sep + index.data()) as file:
                self.fname = self.dir_name + os.sep + index.data()
                self.editor.setPlainText(''.join(file.readlines()))
                self.setWindowTitle(self.fname[self.fname.rfind('/') + 1:])
        except (FileNotFoundError, PermissionError):
            pass

    def save_as_file(self):
        """
        This function asks user to create new file with his
        work (as 'save as' works in other programs)
        :return: None
        """
        self.save_fname = QFileDialog.getSaveFileName(self, 'Save File', '',
                                                      'Text docs (*.txt);;Python files (*.py)')[0]

        try:
            with open(file=self.save_fname, mode='w') as file:
                file.write(self.editor.toPlainText())
                if not hasattr(self, 'fname'):
                    self.fname = self.save_fname
        except FileNotFoundError:
            print('FileNotFoundError.save_as_file')

    def simply_save_file(self):
        """
        This function saves all changes in file which was open (as 'save' in real programs)
        :return: None
        """
        if not hasattr(self, 'fname'):
            self.save_as_file()
            return None
        try:
            with open(file=self.fname, mode='w') as file:
                file.write(self.editor.toPlainText())
        except FileNotFoundError:
            print('FileNotFoundError.simply_save_file')

    def action_change_design_trigered(self):
        """This method calls Widget where user can choose design.
        To make design work use must restart an app.
        :return: None"""
        self.quest = WidgetChangeDesign()
        self.quest.show()

    def update_design(self):
        """
        This method updates design. Design is located in csv file with name 'design.csv'
        :return: None
        """
        design = reading_csv_design(real_path + f'{os.sep}design_csv_table.csv')

        for item, value in design.items():
            if item != 'window':
                try:
                    eval(f'self.{item}.setStyleSheet(\'{value}\')')
                except AttributeError:
                    print('No such attribute', item, sep=' ')
            else:
                self.setStyleSheet(value)

    def copy_last_line(self):
        """
        This method copies last line and pastes it to the end of the text
        :return: None
        """
        text = self.editor.toPlainText()
        if not text:
            return None
        self.editor.setPlainText(text + '\n' + text.split('\n')[-1])
        self.editor.moveCursor(QTextCursor.End)

    def eventFilter(self, obj, event):
        """
        PyQt5 method which defines work keys in all Program
        Need to control working keys in QPlainTextEdit
        :param obj: (QObject) which object has event
        :param event: (QEvent) kind of event
        :return: (bool) True if the operation was successful else False
        """
        if obj is self.editor and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_QuoteDbl:
                # Branch which doubles sign " double quote
                pos_cur = self.editor.textCursor().position()
                text = self.editor.toPlainText()
                new_text = text[:pos_cur] + '\"\"' + text[pos_cur:]
                self.editor.setPlainText(new_text)
                new_cur = QTextCursor(self.editor.document())
                new_cur.setPosition(pos_cur + 1)
                self.editor.setTextCursor(new_cur)
                return True
            elif event.key() == Qt.Key_Apostrophe:
                # Branch which doubles sign ' apostrophe
                pos_cur = self.editor.textCursor().position()
                text = self.editor.toPlainText()
                new_text = text[:pos_cur] + '\'\'' + text[pos_cur:]
                self.editor.setPlainText(new_text)
                new_cur = QTextCursor(self.editor.document())
                new_cur.setPosition(pos_cur + 1)
                self.editor.setTextCursor(new_cur)
                return True
            elif event.key() == Qt.Key_ParenLeft:
                # Branch which doubles () parents
                pos_cur = self.editor.textCursor().position()
                text = self.editor.toPlainText()
                new_text = text[:pos_cur] + '()' + text[pos_cur:]
                self.editor.setPlainText(new_text)
                new_cur = QTextCursor(self.editor.document())
                new_cur.setPosition(pos_cur + 1)
                self.editor.setTextCursor(new_cur)
                return True
            elif event.key() == Qt.Key_Tab:
                # Branch which replace Tab to 4 whitespaces
                pos_cur = self.editor.textCursor().position()
                text = self.editor.toPlainText()
                new_text = text[:pos_cur] + ' ' * 4 + text[pos_cur:]
                self.editor.setPlainText(new_text)
                new_cur = QTextCursor(self.editor.document())
                new_cur.setPosition(pos_cur + 4)
                self.editor.setTextCursor(new_cur)
                return True
            elif event.key() == Qt.Key_BraceLeft:
                # Branch which doubles {}
                pos_cur = self.editor.textCursor().position()
                text = self.editor.toPlainText()
                new_text = text[:pos_cur] + '{}' + text[pos_cur:]
                self.editor.setPlainText(new_text)
                new_cur = QTextCursor(self.editor.document())
                new_cur.setPosition(pos_cur + 1)
                self.editor.setTextCursor(new_cur)
                return True
            elif event.key() == Qt.Key_BracketLeft:
                # Branch which doubles []
                pos_cur = self.editor.textCursor().position()
                text = self.editor.toPlainText()
                new_text = text[:pos_cur] + '[]' + text[pos_cur:]
                self.editor.setPlainText(new_text)
                new_cur = QTextCursor(self.editor.document())
                new_cur.setPosition(pos_cur + 1)
                self.editor.setTextCursor(new_cur)
                return True

        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    ex.show()
    sys.exit(app.exec())
