from player import Player
from random import randint


def roll() -> int:
    return randint(1, 6)


class Game:
    players = []
    dice = []
    current_player = 0
    cur_round = 0

    @classmethod
    def reroll(cls, which_dice: list[bool]) -> None:
        cls.dice = [roll() if do_roll else kosc for do_roll, kosc in zip(which_dice, cls.dice)]

    @classmethod
    def whose_turn(cls) -> Player:
        return cls.players[cls.current_player]

    @classmethod
    def next_turn(cls) -> None:
        if cls.current_player < len(cls.players) - 1:            
            cls.current_player += 1
        else:
            cls.current_player = 0
            cls.cur_round += 1

    @classmethod
    def final(cls) -> list[Player]:
        for player in cls.players:
            player.end()
        sorted_players = sorted(cls.players, key=lambda x: x.score, reverse=True)
        return sorted_players