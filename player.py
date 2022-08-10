from rules import joker, joker_special_scoring, normal_scoring


class Player:
    def __init__(self, name: str=None) -> None:
        self.table = [99 for _ in range(13)]
        self.name = name if name is not None else ''
        self.score = 0

    def scoring(self, dice: list[int], choice: int) -> None:
        sorted_dice = sorted(dice)

        if joker(sorted_dice, self.table[12]):
            self.table[12] += 100
            self.table[choice] = joker_special_scoring(choice, self.table[sorted_dice[0]] != 99)
        else:
            self.table[choice] = normal_scoring(choice, sorted_dice)

    def bonus_text(self) -> str:
        pom_bonus = [x for x in self.table[:6] if x != 99]

        if sum(pom_bonus) < 63:
            return 'To bonus: ' + str(63 - sum(pom_bonus))
        else:
            return 'Bonus achieved'

    def end(self) -> None:
        for x in range(13):
            self.score += self.table[x]
            self.score += 35 if x == 5 and self.score > 62 else 0


def table_text(ind: int, value: int) -> str:
    tables = {
        0: "1:  ",
        1: "2:  ",
        2: "3:  ",
        3: "4:  ",
        4: "5:  ",
        5: "6:  ",
        6: "Chance:  ",
        7: "Three of a kind:  ",
        8: "Small straight:  ",
        9: "Large straight:  ",
        10: "Full House:  ",
        11: "Four of a kind:  ",
        12: "Yahtzee:  ",
    }
    if value == 99:
        return tables[ind] + '0'
    elif value == 0:
        return tables[ind] + '--'
    else:
        return tables[ind] + str(value)
