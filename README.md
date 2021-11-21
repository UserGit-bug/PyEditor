# PyEditor
## Main information
My **first project** on Python, PyEditor - simple editor of Python code.
In development PyQt5 was used.

## Design
All code about design is contained in direstory _\design_.

Design is downloaded from csv tables in main direstory by module
**readingcsvdesign.py**.

In directory _\design_tables_ there are possible designs of main window,
which user can change by his wish

## HighLighter
To highlight code in program I use special QSyntaxHighLighter from PyQt5.
PythonHighLighter is a heritor of QSyntaxHighLighter which is in directory
_\textwork_ in file **codework.py**

## Other files in main directory
File **main.py** runs all program
File **styles.py** make styles for PythonHighLinter in _\textwork_
File **requirements.txt** contains info about modules I used
All **.csv** files contain tables with design for program