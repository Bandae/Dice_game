from PyQt5 import QtCore, QtWidgets
from game import Game, roll
from ui_base_elem import Button
from ui_c_components import CrossoutFrame, InfoFrames, RadioFrame, TransitionFrame, Board, TitleBar, SettingScreen, FinalScreen
import stylesheets


class UiMainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(UiMainWindow, self).__init__()

        self.win_setup()
        self.third_screen_setup()
        self.final_screen = FinalScreen(self.centralwidget)
        SettingScreen(self.centralwidget, lambda: self.main_screen_set_visibility(True))
        TitleBar(self.centralwidget, lambda: self.close())
        self.transition = TransitionFrame(self, self.score2, lambda: self.transition.hide())
        self.crossout_frame = CrossoutFrame(self.centralwidget, self.correct_scoring)

    def third_screen_setup(self) -> None:
        self.score_button = Button(self.centralwidget, 'Score the dice', self.atclick_score, 1050, 604)
        self.score_button.hide()

        self.info_frame = InfoFrames(self.centralwidget)
        self.board = Board(self.centralwidget, lambda: self.crossout_frame.hide(), lambda: self.info_frame.change_info(which_info=2))
        self.radio_frame = RadioFrame(self.centralwidget)

    def win_setup(self) -> None:
        self.resize(1280, 720)
        self.setStyleSheet(stylesheets.WINDOW)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setStyleSheet(stylesheets.GLOBAL_STYLES)
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle("Yahtzee")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def main_screen_set_visibility(self, visible: bool) -> None:
        if visible:
            self.info_frame.set_player(Game.whose_turn().name)

            self.radio_frame.show()
            self.board.show()
            self.board.button_roll.show()
            self.score_button.show()
            self.info_frame.show()

        else:
            self.radio_frame.hide()
            self.board.hide()
            self.board.button_roll.hide()
            self.score_button.hide()
            
            self.info_frame.hide()

    def score2(self) -> None:
        self.info_frame.change_info(which_info=1)
        self.info_frame.set_bonus()
        self.info_frame.set_player(Game.whose_turn().name)

        self.board.reset_button_accept()
        self.board.change_dice_state(reroll=False, disable=False, roll=True)
        self.board.button_roll.show()
        
        self.radio_frame.set_button_text()

    def atclick_score(self) -> None:
        ind, button = self.radio_frame.find_checked()

        Game.whose_turn().scoring(Game.dice, ind)

        self.radio_frame.uncheck(button)

        if Game.whose_turn().table[ind] == 0:
            Game.whose_turn().table[ind] = 99
            self.crossout_frame.help = ind
            self.crossout_frame.show()
        else:
            self.correct_scoring()

    def correct_scoring(self) -> None:
        Game.next_turn()
        self.info_frame.set_round(str(Game.cur_round + 1))

        if Game.cur_round == 13:
            self.transition.play_empty(lambda: self.final_screen.display(lambda: self.main_screen_set_visibility(False)))
        else:
            self.transition.play_normal(Game.whose_turn().name)


if __name__ == "__main__":
    import sys
    Game.dice = [roll() for _ in range(5)]
    app = QtWidgets.QApplication(sys.argv)
    win = UiMainWindow()
    win.show()
    sys.exit(app.exec_())
