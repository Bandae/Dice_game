def joker(dice, yahtzee):
    if yahtzee != 99 and yahtzee != 0 and len(list(set(dice))) == 1:
        return True
    else:
        return False


def joker_special_scoring(choice, is_upper_table_crossed):
    if is_upper_table_crossed:
        if choice == 8:
            return 30
        elif choice == 9:
            return 40
        elif choice == 10:
            return 25
    else:
        return False


def normal_scoring(choice, dice):
    if choice < 6:
        return dice.count(choice + 1) * (choice + 1)
    
    if choice == 6:
        return sum(dice)
    
    if choice == 7:
        if any(dice.count(ind) >= 3 for ind in range(1, 7)):
            return sum(dice)
        else:
            return 0

    if choice == 8:
        dice = list(set(dice))
        if len(dice) >= 4 and all(d_next == d_curr + 1 for d_curr, d_next in zip(dice[:-2], dice[1:-1])):
            return 30
        else:
            return 0
    
    if choice == 9:
        if all(d_next == d_curr + 1 for d_curr, d_next in zip(dice[:-2], dice[1:-1])):
            return 40
        else:
            return 0
    
    if choice == 10:
        if len(list(set(dice))) == 2 and any(dice.count(ind) == 3 for ind in range(1, 7)):
            return 25
        else:
            return 0
    
    if choice == 11:
        if any(dice.count(ind) >= 4 for ind in range(1, 7)):
            return sum(dice)
        else:
            return 0
    
    if choice == 12:
        if len(list(set(dice))) == 1:
            return 50
        else:
            return 0