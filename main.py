import random
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Wpm Test.ui', self)

        self.english_easy_words = []
        self.english_hard_words = []
        self.russian_easy_words = []
        self.russian_hard_words = []

        self.all_words = [self.english_easy_words, self.english_hard_words, self.russian_easy_words,
                          self.russian_hard_words]
        self.all_txt_files = ['english_easy_words.txt', 'english_hard_words.txt', 'russian_easy_words.txt',
                              'russian_hard_words.txt']

        for words in self.all_words:
            with open(self.all_txt_files[self.all_words.index(words)], encoding='utf-8') as f:
                for line in f:
                    for word in line.split(','):
                        if word == line.split(',')[-1]:
                            words.append(word[:-1].lower())
                        elif len(word) > 1:
                            words.append(word.lower())

        self.first_words = [self.word1_1, self.word1_2, self.word1_3, self.word1_4, self.word1_5, self.word1_6]
        self.second_words = [self.word2_1, self.word2_2, self.word2_3, self.word2_4, self.word2_5, self.word2_6]

        for i in self.first_words:
            i.setFont(QFont('Times', 17))
        for i in self.second_words:
            i.setFont(QFont('Times', 17))

        self.btn_1.setStyleSheet("background-color : transparent")
        self.btn_2.setStyleSheet("background-color : transparent")
        self.btn_rewrite.setStyleSheet("background-color : transparent")
        self.btn_switch_lng.setStyleSheet('QPushButton {background-color: #5cb85c; color: white;}')
        self.btn_switch_lng.setFont(QFont("Times", 13))
        self.main_line_edit.setFont(QFont("Times", 17))

        self.flag_rus_words = True
        self.flag_eng_words = False
        self.flag_btn_1 = True
        self.flag_btn_2 = False
        self.btn_flags = [self.flag_btn_1, self.flag_btn_2]
        self.btn_1.clicked.connect(self.switch_level_typing)
        self.btn_2.clicked.connect(self.switch_level_typing)
        self.btn_rewrite.clicked.connect(self.rewrite_text)
        self.btn_switch_lng.clicked.connect(self.switch_language_typing)
        self.main_line_edit.textChanged.connect(self.check_text)
        self.lcd_timer.display(60)
        self.list_first_line = []
        self.list_second_line = []
        self.count = 0
        self.flag_count = 0
        self.ready_words = 0
        self.flag_timer = True
        self.list_value_timer = []
        self.ready_label.hide()
        self.ready_label_num.hide()
        self.rewrite_text()

    def tick_timer(self):
        lcd_value = self.lcd_timer.value()
        self.list_value_timer.append(lcd_value)
        if len(self.list_value_timer) >= 2:
            if self.list_value_timer[-1] >= self.list_value_timer[-2]:
                self.lcd_timer.display(0)
                lcd_value = self.lcd_timer.value()
        if lcd_value > 0:
            self.lcd_timer.display(lcd_value - 1)
            QTimer().singleShot(1000, self.tick_timer)
        elif self.list_value_timer[-1] >= self.list_value_timer[-2]:
            self.ready_words = 0
            self.list_value_timer = []
            self.lcd_timer.display(60)
            self.flag_timer = True
        else:
            self.ready_label.show()
            self.ready_label_num.setText(str(self.ready_words))
            self.ready_label_num.setFont(QFont("Times", 48))
            self.ready_label_num.setStyleSheet("QLabel{color: red}")
            self.ready_label_num.show()
            self.ready_words = 0
            self.list_value_timer = []
            self.main_line_edit.setEnabled(False)
            self.lcd_timer.display(60)
            self.flag_timer = True

    def switch_level_typing(self):
        if self.sender() == self.btn_1:
            self.flag_btn_1 = True
            self.flag_btn_2 = False
            for i in self.first_words:
                i.setFont(QFont("Times", 17))
            for i in self.second_words:
                i.setFont(QFont("Times", 17))
        elif self.sender() == self.btn_2:
            self.flag_btn_1 = False
            self.flag_btn_2 = True
            for i in self.first_words:
                i.setFont(QFont("Times", 13))
            for i in self.second_words:
                i.setFont(QFont("Times", 13))
        self.rewrite_text()

    def switch_language_typing(self):
        if self.flag_rus_words:
            self.flag_rus_words = False
            self.flag_eng_words = True
            self.btn_switch_lng.setText('English')
        else:
            self.flag_rus_words = True
            self.flag_eng_words = False
            self.btn_switch_lng.setText('Russian')
        self.rewrite_text()

    def check_text(self):
        if self.flag_timer:
            self.flag_timer = False
            self.tick_timer()
        if self.count == 6:
            self.list_first_line = self.list_second_line
            counting = 0
            for i in self.list_first_line:
                self.first_words[counting].setText(i)
                self.first_words[counting].setStyleSheet("QLabel{color: black}")
                counting += 1
            self.rewrite_second_line()
            self.count = 0
        elif ' ' in self.main_line_edit.text():
            if self.main_line_edit.text()[:-1] == self.list_first_line[self.count]:
                self.first_words[self.count].setStyleSheet("QLabel{color: green}")
                self.ready_words += 1
            else:
                self.first_words[self.count].setStyleSheet("QLabel{color: red}")
            self.count += 1
            self.main_line_edit.setText('')
        elif self.main_line_edit.text() != self.first_words[self.count]:
            if self.main_line_edit.text() == self.first_words[self.count].text()[:len(self.main_line_edit.text())]:
                self.first_words[self.count].setStyleSheet("QLabel{background-color : #b3b3b3}")
            else:
                self.first_words[self.count].setStyleSheet("QLabel{background-color : red}")

    def rewrite_text(self):
        self.ready_label.hide()
        self.ready_label_num.hide()
        self.main_line_edit.setEnabled(True)
        self.lcd_timer.display(60)
        self.count = 0
        self.ready_words = 0
        self.list_first_line = []
        self.list_second_line = []
        self.main_line_edit.setText('')
        count_words = 0
        if self.flag_btn_1:
            if self.flag_rus_words:
                for i in self.first_words:
                    word_1 = random.choice(self.russian_easy_words)
                    self.first_words[count_words].setText(word_1)
                    self.first_words[count_words].setAlignment(QtCore.Qt.AlignCenter)
                    self.first_words[count_words].setStyleSheet("QLabel{color: black}")
                    self.list_first_line.append(word_1)
                    count_words += 1
                count_words = 0
                for i in self.second_words:
                    word_2 = random.choice(self.russian_easy_words)
                    self.second_words[count_words].setText(word_2)
                    self.second_words[count_words].setAlignment(QtCore.Qt.AlignCenter)
                    self.first_words[count_words].setStyleSheet("QLabel{color: black}")
                    self.list_second_line.append(word_2)
                    count_words += 1
            else:
                for i in self.first_words:
                    word_1 = random.choice(self.english_easy_words)
                    self.first_words[count_words].setText(word_1)
                    self.first_words[count_words].setAlignment(QtCore.Qt.AlignCenter)
                    self.first_words[count_words].setStyleSheet("QLabel{color: black}")
                    self.list_first_line.append(word_1)
                    count_words += 1
                count_words = 0
                for i in self.second_words:
                    word_2 = random.choice(self.english_easy_words)
                    self.second_words[count_words].setText(word_2)
                    self.second_words[count_words].setAlignment(QtCore.Qt.AlignCenter)
                    self.first_words[count_words].setStyleSheet("QLabel{color: black}")
                    self.list_second_line.append(word_2)
                    count_words += 1
        elif self.flag_btn_2:
            if self.flag_rus_words:
                for i in self.first_words:
                    word_1 = random.choice(self.russian_hard_words)
                    self.first_words[count_words].setText(word_1)
                    self.first_words[count_words].setAlignment(QtCore.Qt.AlignCenter)
                    self.first_words[count_words].setStyleSheet("QLabel{color: black}")
                    self.list_first_line.append(word_1)
                    count_words += 1
                count_words = 0
                for i in self.second_words:
                    word_2 = random.choice(self.russian_hard_words)
                    self.second_words[count_words].setText(word_2)
                    self.second_words[count_words].setAlignment(QtCore.Qt.AlignCenter)
                    self.first_words[count_words].setStyleSheet("QLabel{color: black}")
                    self.list_second_line.append(word_2)
                    count_words += 1
            elif self.flag_eng_words:
                for i in self.first_words:
                    word_1 = random.choice(self.english_hard_words)
                    self.first_words[count_words].setText(word_1)
                    self.first_words[count_words].setAlignment(QtCore.Qt.AlignCenter)
                    self.first_words[count_words].setStyleSheet("QLabel{color: black}")
                    self.list_first_line.append(word_1)
                    count_words += 1
                count_words = 0
                for i in self.second_words:
                    word_2 = random.choice(self.english_hard_words)
                    self.second_words[count_words].setText(word_2)
                    self.second_words[count_words].setAlignment(QtCore.Qt.AlignCenter)
                    self.first_words[count_words].setStyleSheet("QLabel{color: black}")
                    self.list_second_line.append(word_2)
                    count_words += 1
        self.flag_count = 0

    def rewrite_second_line(self):
        self.list_second_line = []
        count_words = 0
        if self.flag_rus_words:
            for i in self.second_words:
                word_2 = random.choice(self.russian_easy_words)
                self.second_words[count_words].setText(word_2)
                self.list_second_line.append(word_2)
                count_words += 1
        else:
            for i in self.second_words:
                word_2 = random.choice(self.english_easy_words)
                self.second_words[count_words].setText(word_2)
                self.list_second_line.append(word_2)
                count_words += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.setFixedSize(1296, 327)
    ex.show()
    sys.exit(app.exec())