from collections import Counter


class card:
    rank = 0
    suit = ""
    """
    Initialize a card with rank and suit.
    args: cardRank (int), cardSuit (str)
    11: J, 12: Q, 13: K, 14: A
    """
    def __init__(self, cardRank, cardSuit):
        self.rank = cardRank
        self.suit = cardSuit

    """
    Converts the card to a string, with its rank and suit, with the rank being converted to a single letter if it is 10 or greater
    Args: none
    Returns: string (rank+suit (ex. AS for ace of spaces))
    """
    def __str__(self):
        if 2 <= self.rank and self.rank <= 10:
            return str(self.rank) + self.suit
        elif self.rank == 11:
            return "J" + self.suit
        elif self.rank == 12:
            return "Q" + self.suit
        elif self.rank == 13:
            return "K" + self.suit
        elif self.rank == 14:
            return "A" + self.suit

    """
    Checks if two cards are equal
    Two cards are equal if their suit and rank are equal.
    Args: c (other Card instance)
    Returns: boolean
    """
    def __eq__(self, c):
        if self.rank == c.rank and self.suit == c.suit:
            return True
        return False

def init_card():
    # rank
    while True:
        try:
            rank = input("Enter Rank (2-9, TJQKA): ").strip()
            if rank == "T":
                rank = 10
                break
            elif rank == "J":
                rank = 11
                break
            elif rank == "Q":
                rank = 12
                break
            elif rank == "K":
                rank = 13
                break
            elif rank == "A":
                rank = 14
                break
            rank = int(rank)
            if 2 <= rank <= 9:
                break
            else:
                print("Invalid rank")
        except ValueError:
            print("Invalid input!")
    # suit
    valid_suits = {'S', 'H', 'D', 'C'}  # Spades, Hearts, Diamonds, Clubs
    while True:
        suit = input("Enter Suit (SHDC): ").strip().upper()
        if suit in valid_suits:
            break
        print("Invalid suit!")
    return card(rank, suit)

def init_hand_score(card1, card2):
    r1 = card1.rank
    r2 = card2.rank
    s1 = card1.suit
    s2 = card2.suit
    r3 = max(r1, r2)
    r4 = min(r1, r2)
    ratings = [
        [0,  2,  2,  3,  5,  8,  10, 13, 14, 12, 14, 14, 17],
        [5,  1,  3,  3,  6,  10, 16, 19, 24, 25, 25, 26, 26],
        [8,  9,  1,  5,  6,  10, 19, 26, 28, 29, 29, 30, 31],
        [12, 14, 15, 2,  6,  11, 17, 27, 33, 35, 37, 37, 38],
        [18, 20, 22, 21, 4,  10, 16, 25, 31, 40, 40, 41, 41],
        [32, 35, 36, 34, 31, 7,  17, 24, 29, 38, 47, 47, 49],
        [39, 50, 53, 48, 43, 42, 9,  21, 27, 33, 40, 53, 54],
        [45, 57, 66, 64, 59, 55, 52, 12, 25, 28, 37, 45, 56],
        [51, 60, 71, 80, 74, 68, 61, 57, 16, 27, 29, 38, 49],
        [44, 63, 75, 82, 89, 83, 73, 65, 58, 20, 28, 32, 39],
        [46, 67, 76, 85, 90, 95, 88, 78, 70, 62, 23, 36, 41],
        [49, 67, 77, 86, 92, 96, 98, 93, 81, 72, 76, 23, 46],
        [54, 69, 79, 87, 94, 97, 99,100, 95, 84, 86, 91, 24]
        ]
    if r1 == r2:
        return ratings[14 - r1][14 - r2]
    elif s1 == s2:
        return ratings[14 - r3][14 - r4]
    elif s1 == 14:
        return ratings[14 - r1][14 - r2]
    elif s2 == 14:
        return ratings[14 - r1][14 - r2]
    else:
        return ratings[14 - r4][14 - r3]

def problem0(card1, card2):
    score = init_hand_score(card1, card2)
    print(score)
    if score < 3:
        print("All In!")
    elif score < 6:
        print("Raise 2 times the post")
    elif score < 10:
        print("Raise 3/2 of the post")
    elif score < 20:
        print("Raise the post")
    elif score < 30:
        print("Raise half the post")
    elif score < 80:
        print("Check")
    else:
        print("Fold")

def problem1(card1, card2, table1, table2, table3):
    hand = [card1, card2, table1, table2, table3]
    values = []
    suits = []
    for card in hand:
        values.append(card.rank)
        suits.append(card.suit)
    values = sorted(values)
    suits = sorted(suits)
    counts = Counter(values)
    count_values = sorted(list(counts.values()), reverse=True)
    is_flush = len(set(suits)) == 1
    is_straight = False
    is_four_of_a_kind = False
    is_full_house = False
    is_three_of_a_kind = False
    is_two_pair = False
    is_one_pair = False
    is_high_card = False
    straight_high = 0
    if len(set(values)) == 5 and (values[4] - values[0] == 4):
        is_straight = True
        straight_high = values[4]
    elif values == [2, 3, 4, 5, 14]:
        is_straight = True
        straight_high = 5
    high = values[4]
    is_straight_flush = False
    if is_straight and is_flush:
        is_straight_flush = True
    elif count_values == [4, 1]:
        is_four_of_a_kind = True
    elif count_values == [3, 2]:
        is_full_house = True
#flush
#straight
    elif count_values == [3, 1, 1]:
        is_three_of_a_kind = True
    elif count_values == [2, 2, 1]:
        is_two_pair = True
    elif count_values == [2, 1, 1, 1]:
        is_one_pair = True
    else:
        is_high_card = True
    score = 0
    if is_straight_flush:
        score = 14 - straight_high # 9
    elif is_four_of_a_kind:
        score = 24 - high # 22
    elif is_full_house:
        score = 37 - high # 34
    elif is_flush:
        score = 49 - high # 47
    elif is_straight:
        score = 62 - straight_high # 57
    elif is_three_of_a_kind:
        score = 72 - high # 70
    elif is_two_pair:
        score = 84 - high # 82
    elif is_one_pair:
        score = 97 - high # 95
    elif is_high_card :
        score = 110 - high # 108
    print(score)
    if score < 50:
        print("All In!")
    elif score < 60:
        print("Raise 2 times the post")
    elif score < 70:
        print("Raise 3/2 of the post")
    elif score < 80:
        print("Raise the post")
    elif score < 90:
        print("Raise half the post")
    elif score < 100:
        print("Check")
    else:
        print("Fold")


def problem2(card1, card2, table1, table2, table3, table4):
    hand = [card1, card2, table1, table2, table3, table4]
    values = []
    suits = []
    for card in hand:
        values.append(card.rank)
        suits.append(card.suit)
    values = sorted(values)
    suits = sorted(suits)
    counts = Counter(values)
    count_values = sorted(list(counts.values()), reverse=True)
    suit_counts = Counter(suits)
    is_flush = any(count >= 5 for count in suit_counts.values())
    is_straight = False
    is_four_of_a_kind = False
    is_full_house = False
    is_three_of_a_kind = False
    is_two_pair = False
    is_one_pair = False
    is_high_card = False
    straight_high = 0

    # straight
    sortiert = sorted(list(set(values)))
    # Check standard straights
    for i in range(len(sortiert) - 4):
        if sortiert[i + 4] - sortiert[i] == 4:
            is_straight = True
            straight_high = max(straight_high, sortiert[i + 4])
    # acelow
    if all(x in values for x in [2, 3, 4, 5, 14]):
        is_straight = True
        straight_high = max(straight_high, 5)
    high = values[5]
    is_straight_flush = False
    # straightflush
    if is_straight and is_flush:
        # Verify if the same 5 cards make both the straight and the flush
        # Group cards by suit to check if any single suit has a 5-card straight
        cards_by_suit = {}
        for card in hand:
            cards_by_suit.setdefault(card.suit, []).append(card.rank)
        for suit_ranks in cards_by_suit.values():
            if len(suit_ranks) >= 5:
                s_vals = sorted(list(set(suit_ranks)))
                for i in range(len(s_vals) - 4):
                    if s_vals[i + 4] - s_vals[i] == 4:
                        is_straight_flush = True
                if all(x in s_vals for x in [2, 3, 4, 5, 14]):
                    is_straight_flush = True
    elif count_values[0] == 4:
        is_four_of_a_kind = True
    elif count_values[0] == 3 and count_values[1] >= 2:
        is_full_house = True
    elif count_values == [3, 3] or (len(count_values) >= 3 and count_values[0] == 3 and count_values[1] == 1):
        is_three_of_a_kind = True
    elif (count_values[0] == 2 and count_values[1] == 2):
        is_two_pair = True
    elif count_values[0] == 2:
        is_one_pair = True
    else:
        is_high_card = True
    score = 0
    if is_straight_flush:
        score = 14 - straight_high # 9
    elif is_four_of_a_kind:
        score = 24 - high # 22
    elif is_full_house:
        score = 37 - high # 34
    elif is_flush:
        score = 49 - high # 47
    elif is_straight:
        score = 62 - straight_high # 57
    elif is_three_of_a_kind:
        score = 72 - high # 70
    elif is_two_pair:
        score = 84 - high # 82
    elif is_one_pair:
        score = 97 - high # 95
    elif is_high_card :
        score = 110 - high # 108
    print(score)
    if score < 40:
        print("All In!")
    elif score < 50:
        print("Raise 2 times the post")
    elif score < 60:
        print("Raise 3/2 of the post")
    elif score < 70:
        print("Raise the post")
    elif score < 80:
        print("Raise half the post")
    elif score < 90:
        print("Check")
    else:
        print("Fold")

def problem3(card1, card2, table1, table2, table3, table4, table5):
    hand = [card1, card2, table1, table2, table3, table4, table5]
    values = []
    suits = []
    for card in hand:
        values.append(card.rank)
        suits.append(card.suit)
    values = sorted(values)
    suits = sorted(suits)
    counts = Counter(values)
    count_values = sorted(list(counts.values()), reverse=True)

    # Flush: 5 or more cards of the same suit in a 7-card hand
    suit_counts = Counter(suits)
    is_flush = any(count >= 5 for count in suit_counts.values())

    is_straight = False
    is_four_of_a_kind = False
    is_full_house = False
    is_three_of_a_kind = False
    is_two_pair = False
    is_one_pair = False
    is_high_card = False
    straight_high = 0

    # Straight check for 7 cards (looking for any 5 consecutive values)
    unique_vals = sorted(list(set(values)))
    for i in range(len(unique_vals) - 4):
        if unique_vals[i + 4] - unique_vals[i] == 4:
            is_straight = True
            straight_high = max(straight_high, unique_vals[i + 4])
    # Check Ace-low straight (A, 2, 3, 4, 5)
    if all(x in values for x in [2, 3, 4, 5, 14]):
        is_straight = True
        straight_high = max(straight_high, 5)

    high = values[6]
    is_straight_flush = False

    # Straight Flush check
    if is_straight and is_flush:
        # Group cards by suit to check if any single suit has a 5-card straight
        cards_by_suit = {}
        for card in hand:
            cards_by_suit.setdefault(card.suit, []).append(card.rank)
        for suit_ranks in cards_by_suit.values():
            if len(suit_ranks) >= 5:
                s_vals = sorted(list(set(suit_ranks)))
                for i in range(len(s_vals) - 4):
                    if s_vals[i + 4] - s_vals[i] == 4:
                        is_straight_flush = True
                if all(x in s_vals for x in [2, 3, 4, 5, 14]):
                    is_straight_flush = True

    # Pattern matching on counts for a 7-card hand
    elif count_values[0] == 4:
        is_four_of_a_kind = True
    elif count_values[0] == 3 and count_values[1] >= 2:
        is_full_house = True
    elif count_values[0] == 3 and count_values[1] < 2:
        is_three_of_a_kind = True
    elif count_values[0] == 2 and count_values[1] == 2:
        is_two_pair = True
    elif count_values[0] == 2:
        is_one_pair = True
    else:
        is_high_card = True
    score = 0
    if is_straight_flush:
        score = 14 - straight_high # 9
    elif is_four_of_a_kind:
        score = 24 - high # 22
    elif is_full_house:
        score = 37 - high # 34
    elif is_flush:
        score = 49 - high # 47
    elif is_straight:
        score = 62 - straight_high # 57
    elif is_three_of_a_kind:
        score = 72 - high # 70
    elif is_two_pair:
        score = 84 - high # 82
    elif is_one_pair:
        score = 97 - high # 95
    elif is_high_card :
        score = 110 - high # 108
    print(score)
    if score < 30:
        print("All In!")
    elif score < 40:
        print("Raise 2 times the post")
    elif score < 50:
        print("Raise 3/2 of the post")
    elif score < 60:
        print("Raise the post")
    elif score < 70:
        print("Raise half the post")
    elif score < 80:
        print("Check")
    else:
        print("Fold")




"""
c1 = card(14, "C")  # Ace of Spades
c2 = card(14, "C")  # King of Hearts
c3 = card(14, "C")
c4 = card(14, "C")
c5 = card(5, "S")
c6 = card(5, "C")
"""
c1 = init_card()
c2 = init_card()
problem0(c1,c2)
c3 = init_card()
c4 = init_card()
c5 = init_card()
problem1(c1, c2, c3, c4, c5)
c6 = init_card()
problem2(c1, c2, c3, c4, c5, c6)
c7 = init_card()
problem3(c1, c2, c3, c4, c5, c6, c7)




