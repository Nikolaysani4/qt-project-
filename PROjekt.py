import sys
import pyglet
import sqlite3
import typing

from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication
from PyQt5.QtCore import Qt

from main_window import Ui_MainWindow
from piano_ui import Ui_Piano
from settings import Ui_Settings
from swap_tool import Ui_SwapTool

con = sqlite3.connect('my_piano.db')
cur = con.cursor()

tool = "piano"
volume = 1


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.quit_btn.clicked.connect(self.close)
        self.start_btn.clicked.connect(self.open_piano)
        self.settings_btn.clicked.connect(self.open_settings)

    def open_piano(self):
        """
        открытие окна пианино
        :return:
        """
        piano_dialog = Piano(self)
        piano_dialog.exec_()

    def open_settings(self):
        """
        открытие окна настроек
        :return:
        """
        settings_dialog = Settings()
        settings_dialog.exec_()


def get_notes_path(table_name) -> typing.List[str]:
    """
    получение информации из базы данных
    :param table_name:
    :return:
    """
    notes_from_db = cur.execute(f"select * from {table_name}").fetchall()
    return [item[1] for item in notes_from_db]


class Piano(QDialog, Ui_Piano):
    def __init__(self, main):
        """
        иницализации класса
        :param main:
        """
        super().__init__()
        self.setupUi(self)
        self.back_btn.clicked.connect(self.close)
        # self.piano_settings_btn.clicked.connect(main.open_settings)
        self.notes = get_notes_path(tool)
        self.piano_settings_btn.hide()

    def keyPressEvent(self, event):
        """
        считывание клавиш с клавиатуры
        :param event:
        :return:
        """
        if event.key() == Qt.Key_Q:
            player = pyglet.media.load(self.notes[0]).play()
            player.volume = volume
        elif event.key() == Qt.Key_W:
            player = pyglet.media.load(self.notes[1]).play()
            player.volume = volume
        elif event.key() == Qt.Key_E:
            player = pyglet.media.load(self.notes[2]).play()
            player.volume = volume
        elif event.key() == Qt.Key_R:
            player = pyglet.media.load(self.notes[3]).play()
            player.volume = volume
        elif event.key() == Qt.Key_T:
            player = pyglet.media.load(self.notes[4]).play()
            player.volume = volume
        elif event.key() == Qt.Key_Y:
            player = pyglet.media.load(self.notes[5]).play()
            player.volume = volume
        elif event.key() == Qt.Key_U:
            player = pyglet.media.load(self.notes[6]).play()
            player.volume = volume


class Settings(QDialog, Ui_Settings):
    def __init__(self):
        """
        инициализация класса
        """
        super().__init__()
        self.setupUi(self)
        self.return_btn.clicked.connect(self.close)
        self.switch_btn.clicked.connect(self.open_swap_tool)
        self.volume_slider.valueChanged.connect(self.onValueChanged)

    def open_swap_tool(self):
        """
        открытие окна смены инструмента
        :return:
        """
        swap_tool_dialog = SwapTool()
        swap_tool_dialog.exec_()

    def onValueChanged(self, volume_):
        """
        громкость
        :param volume_:
        :return:
        """
        global volume

        volume = volume_


class SwapTool(QDialog, Ui_SwapTool):
    def __init__(self):
        """
        инициализации класса
        """
        super().__init__()
        self.setupUi(self)
        self.back_to_settings_btn.clicked.connect(self.close)
        self.tool = ""
        self.piano_swap_btn.clicked.connect(lambda: self.swap_tool("piano"))
        self.saxophone_swap_btn.clicked.connect(lambda: self.swap_tool("saxophone"))
        self.trombone_swap_btn.clicked.connect(lambda: self.swap_tool("trombone"))
        self.violin_swap_btn.clicked.connect(lambda: self.swap_tool("violin"))
        self.guitar_swap_btn.clicked.connect(lambda: self.swap_tool("guitar"))
        self.clarinet_swap_btn.clicked.connect(lambda: self.swap_tool("clarinet"))

        self.piano_swap_btn.clicked.connect(lambda: self.label_tool.setText("PIANO"))
        self.saxophone_swap_btn.clicked.connect(lambda: self.label_tool.setText("SAXOPHONE"))
        self.trombone_swap_btn.clicked.connect(lambda: self.label_tool.setText("TROMBONE"))
        self.violin_swap_btn.clicked.connect(lambda: self.label_tool.setText("VIOLIN"))
        self.guitar_swap_btn.clicked.connect(lambda: self.label_tool.setText("GUITAR"))
        self.clarinet_swap_btn.clicked.connect(lambda: self.label_tool.setText("CLARINET"))

    def swap_tool(self, tool_):
        """
        смена инструмента
        :param tool_:
        :return:
        """
        global tool
        self.tool = tool_
        tool = tool_


def except_hook(cls, exception, traceback):
    """
    ловитель ошибок
    :param cls:
    :param exception:
    :param traceback:
    :return:
    """
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
