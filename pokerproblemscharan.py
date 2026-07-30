import itertools

FOLD = "Fold"
CHECK = "Check"
RAISE_HALF = "Raise half the pot"
RAISE_POT = "Raise the pot"
RAISE_3_2 = "Raise 3/2 of the pot"
RAISE_2X = "Raise 2 times the pot"
ALL_IN = "All In"

DECISION_ORDER = [FOLD, CHECK, RAISE_HALF, RAISE_POT, RAISE_3_2, RAISE_2X, ALL_IN]

POSITION_BONUS = {
    "early": -1,
    "middle": 0,
    "late": 1,
    "button": 2,
}

RANK_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
    "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14
}


def parse_card(text):
    text = text.strip().upper()
    rank_value = RANK_VALUES[text[0]]
    suit_char = text[1]
    return (rank_value, suit_char)


def ask_for_cards(how_many, description):
    cards = []
    print(f"Enter your {how_many} {description}, one at a time.")
    for i in range(how_many):
        text = input(f"  Card {i + 1}: ")
        cards.append(parse_card(text))
    return cards


def ask_for_position():
    print("What's your position at the table? (early, middle, late, button)")
    position = input("  Position: ").strip().lower()
    if position not in POSITION_BONUS:
        position = "middle"
    return position


def apply_position_adjustment(decision, position):
    bonus = POSITION_BONUS[position]
    index = DECISION_ORDER.index(decision)
    new_index = index + bonus
    new_index = max(0, min(new_index, len(DECISION_ORDER) - 1))
    return DECISION_ORDER[new_index]


def rate_starting_hand(cards):
    (r1, s1), (r2, s2) = cards
    high = max(r1, r2)
    low = min(r1, r2)
    points = 0

    if high > 10:
        points += (high - 10) * 2
    if low > 10:
        points += (low - 10)
    if r1 == r2:
        points += 10 + r1
    if s1 == s2:
        points += 2

    gap = high - low
    if gap == 1:
        points += 2
    elif gap == 2:
        points += 1

    return points


def decision_from_points(points):
    if points >= 30:
        return ALL_IN
    elif points >= 24:
        return RAISE_2X
    elif points >= 18:
        return RAISE_3_2
    elif points >= 13:
        return RAISE_POT
    elif points >= 8:
        return RAISE_HALF
    elif points >= 4:
        return CHECK
    else:
        return FOLD


def program1():
    print("\n Program 1: Rate your 2 hole cards (pre-flop)")
    hole_cards = ask_for_cards(2, "hole cards")
    position = ask_for_position()
    points = rate_starting_hand(hole_cards)
    decision = decision_from_points(points)
    decision = apply_position_adjustment(decision, position)
    print(f"\nHand strength points: {points}")
    print(f"Position: {position}")
    print(f"Suggested action: {decision}")


def score_five_cards(five_cards):
    ranks = sorted((c[0] for c in five_cards), reverse=True)
    suits = [c[1] for c in five_cards]
    is_flush = len(set(suits)) == 1

    unique_ranks = sorted(set(ranks), reverse=True)
    is_straight = False
    straight_high = None
    if len(unique_ranks) == 5:
        if unique_ranks[0] - unique_ranks[4] == 4:
            is_straight = True
            straight_high = unique_ranks[0]
        elif unique_ranks == [14, 5, 4, 3, 2]:
            is_straight = True
            straight_high = 5

    counts = {}
    for r in ranks:
        counts[r] = counts.get(r, 0) + 1

    count_items = sorted(counts.items(), key=lambda item: (item[1], item[0]), reverse=True)
    ordered_ranks = [rank for rank, count in count_items]
    count_pattern = [count for rank, count in count_items]

    if is_straight and is_flush:
        return (8, straight_high)
    if count_pattern == [4, 1]:
        return (7, ordered_ranks[0], ordered_ranks[1])
    if count_pattern == [3, 2]:
        return (6, ordered_ranks[0], ordered_ranks[1])
    if is_flush:
        return (5, ranks)
    if is_straight:
        return (4, straight_high)
    if count_pattern == [3, 1, 1]:
        return (3, ordered_ranks[0], ordered_ranks[1], ordered_ranks[2])
    if count_pattern == [2, 2, 1]:
        return (2, ordered_ranks[0], ordered_ranks[1], ordered_ranks[2])
    if count_pattern == [2, 1, 1, 1]:
        return (1, ordered_ranks[0], ordered_ranks[1], ordered_ranks[2], ordered_ranks[3])
    return (0, ranks)


def best_hand_score(all_known_cards):
    best = None
    for five_cards in itertools.combinations(all_known_cards, 5):
        score = score_five_cards(five_cards)
        if best is None or score > best:
            best = score
    return best


HAND_NAMES = {
    0: "High Card",
    1: "One Pair",
    2: "Two Pair",
    3: "Three of a Kind",
    4: "Straight",
    5: "Flush",
    6: "Full House",
    7: "Four of a Kind",
    8: "Straight Flush",
}


def decision_from_category(category, cards_known):
    if cards_known == 3:
        table = {
            0: FOLD, 1: CHECK, 2: RAISE_HALF, 3: RAISE_POT,
            4: RAISE_POT, 5: RAISE_3_2, 6: RAISE_2X, 7: ALL_IN, 8: ALL_IN,
        }
    elif cards_known == 4:
        table = {
            0: FOLD, 1: CHECK, 2: RAISE_HALF, 3: RAISE_3_2,
            4: RAISE_3_2, 5: RAISE_2X, 6: RAISE_2X, 7: ALL_IN, 8: ALL_IN,
        }
    else:
        table = {
            0: FOLD, 1: CHECK, 2: RAISE_POT, 3: RAISE_3_2,
            4: RAISE_2X, 5: RAISE_2X, 6: ALL_IN, 7: ALL_IN, 8: ALL_IN,
        }
    return table[category]


def rate_hand_with_table_cards(num_table_cards):
    hole_cards = ask_for_cards(2, "hole cards")
    table_cards = ask_for_cards(num_table_cards, "table cards")
    position = ask_for_position()
    all_cards = hole_cards + table_cards

    score = best_hand_score(all_cards)
    category = score[0]
    decision = decision_from_category(category, num_table_cards)
    decision = apply_position_adjustment(decision, position)

    print(f"\nBest hand so far: {HAND_NAMES[category]}")
    print(f"Position: {position}")
    print(f"Suggested action: {decision}")


def program2():
    print("\nProrgam 2: Rate your hand after the flop (3 table cards)")
    rate_hand_with_table_cards(3)


def program3():
    print("\nProgram 3: Rate your hand after the turn (4 table cards)")
    rate_hand_with_table_cards(4)


def program4():
    print("\n Program 4: Rate your hand after the river (5 table cards)")
    rate_hand_with_table_cards(5)


def main():
    while True:
        print(" Texas Hold'em Hand Rater")
        print("1) Rate 2 hole cards (pre-flop)")
        print("2) Rate hole cards + 3 table cards (flop)")
        print("3) Rate hole cards + 4 table cards (turn)")
        print("4) Rate hole cards + 5 table cards (river)")
        print("5) Quit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            program1()
        elif choice == "2":
            program2()
        elif choice == "3":
            program3()
        elif choice == "4":
            program4()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
