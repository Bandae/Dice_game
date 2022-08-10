from typing import Callable
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
import stylesheets
from player import table_text, Player
from game import Game
from ui_base_elem import FrameWithLabel, Button, SpinBox, Entry


class SettingScreen:
    def __init__(self, master: QWidget, show_main_screen: Callable) -> None:
        self.info_frame = FrameWithLabel(master, 'Choose amount of players (1 - 5)', [150, 440, 300, 40])
        self.info_frame.show()
        
        self.accept_button = Button(master, 'Accept', lambda: self.atclick_accept1(show_main_screen), 200, 560)

        self.spin_box = SpinBox(master)

        self.picture = QtWidgets.QLabel(master)
        self.picture.setGeometry(QtCore.QRect(545, 58, 640, 604))
        self.picture.setPixmap(QtGui.QPixmap("img/gambling_with_death_T.png"))

        self.entry_list = [Entry(master, 210 + 70 * ind) for ind in range(5)]
        
    def atclick_accept1(self, show_main_screen: Callable) -> None:
        if self.spin_box.value():
            self.spin_box.deleteLater()
            self.info_frame.deleteLater()

            self.accept_button.clicked.disconnect()
            self.accept_button.clicked.connect(lambda: self.atclick_accept2(show_main_screen))

            for ind in range(self.spin_box.value()):
                self.entry_list[ind].show()
                Game.players.append(Player())

    def atclick_accept2(self, show_main_screen: Callable) -> None:
        for ind, player in enumerate(Game.players):
            player.name = self.entry_list[ind].displayText()
            self.entry_list[ind].deleteLater()
        
        self.picture.deleteLater()
        self.accept_button.deleteLater()

        show_main_screen()


class FinalScreen:
    def __init__(self, master: QWidget) -> None:
        self.last_screen_frame1 = []
        self.last_screen_frame2 = []
        self.last_screen_frame3 = []
        player_header_frame = FrameWithLabel(master, 'Player:', [460, 100, 300, 40])
        self.last_screen_frame2.append(player_header_frame)
        
        score_header_frame = FrameWithLabel(master, 'Score:', [780, 100, 100, 40])
        self.last_screen_frame3.append(score_header_frame)

        for ind in range(5):
            number_frame = FrameWithLabel(master, str(ind + 1), [395, 160 + 60 * ind, 50, 40])
            self.last_screen_frame1.append(number_frame)

            player_name_frame = FrameWithLabel(master, '', [460, 160 + 60 * ind, 300, 40])
            self.last_screen_frame2.append(player_name_frame)

            player_score_frame = FrameWithLabel(master, '', [780, 160 + 60 * ind, 100, 40])
            self.last_screen_frame3.append(player_score_frame)
    
    def display(self, hide_main_screen: Callable) -> None:
        hide_main_screen()

        sorted_players = Game.final()
        self.last_screen_frame2[0].show()
        self.last_screen_frame3[0].show()

        for ind, player in enumerate(sorted_players):
            self.last_screen_frame2[ind + 1].label.setText(player.name)
            self.last_screen_frame3[ind + 1].label.setText(str(player.score))
            
            self.last_screen_frame1[ind].show()
            self.last_screen_frame2[ind + 1].show()
            self.last_screen_frame3[ind + 1].show()


class InfoFrames(QtWidgets.QFrame):
    def __init__(self, master: QWidget) -> None:
        super().__init__(master)
        self.setGeometry(QtCore.QRect(0, 0, 700, 120))
        self.hide()
        
        self.player = FrameWithLabel(self, '', [20, 20, 200, 40], hide=False)
        self.round = FrameWithLabel(self, 'Round:  1', [240, 20, 100, 40], hide=False)
        self.bonus = FrameWithLabel(self, 'To bonus: 63', [360, 20, 200, 40], hide=False)
        self.info1 = FrameWithLabel(self, 'Pick dice for reroll, or score the dice', [200, 80, 500, 40], hide=False)
        self.info2 = FrameWithLabel(self, 'Score the dice', [480, 80, 200, 40])
    
    def set_player(self, name: str) -> None:
        self.player.label.setText(name)
    
    def set_round(self, cur_round: int) -> None:
        self.round.label.setText('Round:  ' + cur_round)
    
    def set_bonus(self) -> None:
        text = Game.whose_turn().bonus_text()
        self.bonus.label.setText(text)

    def change_info(self, which_info: int) -> None:        
        if which_info == 1:
            self.info2.hide()
            self.info1.show()
        else:
            self.info1.hide()
            self.info2.show()


class CrossoutFrame(FrameWithLabel):
    def __init__(self, master: QWidget, callback: Callable):
        super().__init__(master, 'Are you sure you want to score 0 points?', [410, 250, 460, 220], [20, 20, 420, 80], stylesheets.CROSSOUT_FRAME)
        
        self.help = 0
        self.callback = callback

        self.crossout_button_yes = Button(self, 'Yes', self.atclick_crossout_yes, 20, 120)
        self.crossout_button_no = Button(self, 'No', lambda: self.hide(), 240, 120)

    def atclick_crossout_yes(self) -> None:
        Game.whose_turn().table[self.help] = 0
        self.hide()
        self.callback()


class RadioFrame(QtWidgets.QFrame):
    def __init__(self, master: QWidget) -> None:
        super().__init__(master)
        self.setGeometry(QtCore.QRect(1050, 36, 200, 530))
        self.setStyleSheet(stylesheets.CHOICE_FRAME)
        self.hide()
        self.buttons = []
        self.group = QtWidgets.QButtonGroup(self)
        # add scoring button here

        for ind in range(13):
            r_button = QtWidgets.QRadioButton(self)
            r_button.setGeometry(QtCore.QRect(10, 10 + 40 * ind, 180, 40))
            r_button.setText(table_text(ind, 99))
            r_button.setFont(stylesheets.DEFAULT_FONT)

            self.buttons.append(r_button)
            self.group.addButton(r_button)
    
    def find_checked(self) -> tuple[int, Button]:
        for ind, button in enumerate(self.buttons):
            if button.isChecked():
                return (ind, button)
    
    def uncheck(self, button: Button) -> None:
        self.group.setExclusive(False)
        button.setChecked(False)
        self.group.setExclusive(True)

    def set_button_text(self) -> None:
        for ix, button in enumerate(self.buttons):
            button.setText(table_text(ix, Game.whose_turn().table[ix]))
            if Game.whose_turn().table[ix] == 99:
                button.setEnabled(True)
            else:
                button.setEnabled(False)


class Board(QtWidgets.QFrame):
    def __init__(self, master: QWidget, hide_crossout: Callable, change_info: Callable) -> None:
        super().__init__(master)
        self.setGeometry(QtCore.QRect(200, 140, 759, 508))
        self.setStyleSheet(stylesheets.BOARD)
        self.hide()
        self.dice = []
        self.button_roll = Button(master, 'Second throw', self.atclick_throw_2, 759, 40)
        self.button_roll.hide()

        self.hide_crossout = hide_crossout
        self.change_info = change_info


        self.pos_dice = {
            0: (30, 30),
            1: (273, 30),
            2: (516, 30),
            3: (152, 269),
            4: (394, 269)
        }

        for ind in range(5):
            self.dice.append(QtWidgets.QPushButton(self))
            self.dice[ind].setGeometry(QtCore.QRect(self.pos_dice[ind][0], self.pos_dice[ind][1], 213, 209))
            self.dice[ind].setStyleSheet(stylesheets.DICE_BUTTON)

            self.dice[ind].setIconSize(QtCore.QSize(211, 203))
            self.dice[ind].setCheckable(True)
        
        self.change_dice_state(reroll=False, roll=True, disable=False)
        
    def set_dice_icons(self, dice_values: list[int]) -> None:
        for die, value in zip(self.dice, dice_values):
            die.setIcon(QtGui.QIcon(QtGui.QPixmap(stylesheets.ICONS[value])))
    
    def change_dice_state(self, reroll: bool, roll: bool, disable: bool) -> None:
        if reroll:
            which_dice = [die.isChecked() for die in self.dice]
            Game.reroll(which_dice)
        
        [die.setChecked(False) for die in self.dice]
        [die.setDisabled(disable) for die in self.dice]
        
        if roll:
            Game.reroll([True for _ in self.dice])
        
        self.set_dice_icons(Game.dice)

    def any_dice_checked(self) -> bool:
        return any([die.isChecked() for die in self.dice])

    def atclick_throw_2(self) -> None:
        if self.any_dice_checked():
            self.hide_crossout()

            self.button_roll.clicked.disconnect()
            self.button_roll.setText('Third throw')
            self.button_roll.clicked.connect(self.atclick_throw_3)

            self.change_dice_state(reroll=True, disable=False, roll=False)

    def atclick_throw_3(self) -> None:
        if self.any_dice_checked():

            self.hide_crossout()
            self.button_roll.hide()

            self.change_info()
            self.change_dice_state(reroll=True, disable=True, roll=False)

    def reset_button_accept(self) -> None:
        self.button_roll.clicked.disconnect()
        self.button_roll.setText('Second throw')
        self.button_roll.clicked.connect(self.atclick_throw_2)


class TransitionFrame(FrameWithLabel):
    def __init__(self, master: QWidget, callback1: Callable, callback2: Callable) -> None:
        super().__init__(master, '', [0, 0, 1280, 720], style=stylesheets.TRANSITION_BG)
        self.label.setFont(stylesheets.TRANSITION_FONT)

        fade = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(fade)
        
        self.anim = QtCore.QPropertyAnimation(fade, b"opacity")
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setDuration(500)
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        anim_2 = QtCore.QPropertyAnimation(fade, b"opacity")
        anim_2.setStartValue(1)
        anim_2.setEndValue(1)
        anim_2.setDuration(500)

        anim_3 = QtCore.QPropertyAnimation(fade, b"opacity")
        anim_3.setStartValue(1)
        anim_3.setEndValue(0)
        anim_3.setDuration(500)
        anim_3.setEasingCurve(QtCore.QEasingCurve.InCubic)

        self.animations = QtCore.QSequentialAnimationGroup()
        self.animations.addAnimation(self.anim)
        self.animations.addAnimation(anim_2)
        self.animations.addAnimation(anim_3)

        self.anim.finished.connect(callback1)
        self.animations.finished.connect(callback2)

    def play_normal(self, text: str) -> None:
        self.label.setText(text)
        self.show()
        self.animations.start()

    def play_empty(self, callback: Callable) -> None:
        self.label.setText('')
        self.show()
        self.animations.start()
        self.anim.finished.connect(callback)


class TitleBar():
    def __init__(self, master: QWidget, window_close_fn: Callable) -> None:
        frame_exit = FrameWithLabel(master, 'Are you sure you want to quit?', [410, 250, 460, 220], [20, 20, 420, 80], stylesheets.EXIT_FRAME)

        self.button_exit = QtWidgets.QPushButton(master)
        self.button_exit.setGeometry(QtCore.QRect(1250, 10, 20, 20))
        self.button_exit.clicked.connect(lambda: frame_exit.show())
        self.button_exit.setStyleSheet(stylesheets.EXIT_BUTTON)

        self.button_help = QtWidgets.QPushButton(master)
        self.button_help.setGeometry(QtCore.QRect(1220, 10, 20, 20))
        self.button_help.clicked.connect(lambda: self.atclick_help())
        self.button_help.setStyleSheet(stylesheets.HELP_BUTTON)

        self.scroll_help = QtWidgets.QScrollArea(master)
        self.scroll_help.setGeometry(QtCore.QRect(20, 20, 1240, 680))
        self.scroll_help.setWidgetResizable(True)
        self.scroll_help.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_help.hide()

        self.frame_help = QtWidgets.QFrame(self.scroll_help)
        self.frame_help.setMinimumSize(1200, 1700)

        self.label_help = QtWidgets.QLabel(self.frame_help)
        self.label_help.setGeometry(QtCore.QRect(280, 0, 640, 1700))
        self.label_help.setPixmap(QtGui.QPixmap("img/rules.png"))

        self.scroll_help.setWidget(self.frame_help)

        self.button_back_help = QtWidgets.QPushButton(self.scroll_help)
        self.button_back_help.setGeometry(QtCore.QRect(5, 5, 40, 20))
        self.button_back_help.clicked.connect(self.atclick_back_help)
        self.button_back_help.setIcon(QtGui.QIcon(QtGui.QPixmap("img/back.svg")))
        self.button_back_help.setStyleSheet(stylesheets.DEFAULT_BUTTON)

        button_ex_yes = Button(frame_exit, 'Yes', window_close_fn, 20, 120)
        button_ex_no = Button(frame_exit, 'No', lambda: frame_exit.hide(), 240, 120)

    def atclick_help(self) -> None:
        self.button_help.hide()
        self.button_exit.hide()
        self.scroll_help.show()

    def atclick_back_help(self) -> None:
        self.scroll_help.hide()
        self.button_help.show()
        self.button_exit.show()
