# Rank Mapping


RANKS = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}

REVERSE_RANKS = {value: key for key, value in RANKS.items()}

VALID_SUITS = {"S", "H", "D", "C"}


# Card Parsing

def parse_card(card):
    """
    Converts a card string into (rank, suit).
    """

    card = card.upper().strip()

    rank = card[:-1]
    suit = card[-1]

    if rank not in RANKS:
        raise ValueError(f"Invalid rank: {rank}")

    if suit not in VALID_SUITS:
        raise ValueError(f"Invalid suit: {suit}")

    return (RANKS[rank], suit)


def parse_cards(card_list):
    return [parse_card(card) for card in card_list]


# Card Display Helpers

def card_to_string(card):
    return f"{REVERSE_RANKS[card[0]]}{card[1]}"


def cards_to_string(cards):
    return " ".join(card_to_string(card) for card in cards)


def rank_name(rank):
    names = {
        14: "Ace",
        13: "King",
        12: "Queen",
        11: "Jack",
        10: "Ten",
        9: "Nine",
        8: "Eight",
        7: "Seven",
        6: "Six",
        5: "Five",
        4: "Four",
        3: "Three",
        2: "Two"
    }

    return names[rank]


# Validation

def validate_unique_cards(hole_cards, board_cards):
    all_cards = hole_cards + board_cards

    if len(all_cards) != len(set(all_cards)):
        raise ValueError("Duplicate cards detected.")


# Straight Detection

def is_straight(ranks):
    unique = sorted(set(ranks))

    if len(unique) < 5:
        return False, None

    for i in range(len(unique) - 4):

        window = unique[i:i + 5]

        if window == list(range(window[0], window[0] + 5)):
            return True, window[-1]

    # Wheel straight
    if {14, 2, 3, 4, 5}.issubset(unique):
        return True, 5

    return False, None


# Rank Mapping

RANKS = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}

REVERSE_RANKS = {value: key for key, value in RANKS.items()}

VALID_SUITS = {"S", "H", "D", "C"}


# Card Parsing


def parse_card(card):
    card = card.upper().strip()

    rank = card[:-1]
    suit = card[-1]

    if rank not in RANKS:
        raise ValueError(f"Invalid rank: {rank}")

    if suit not in VALID_SUITS:
        raise ValueError(f"Invalid suit: {suit}")

    return (RANKS[rank], suit)


def parse_cards(card_list):
    return [parse_card(card) for card in card_list]


# Card Display Helpers


def card_to_string(card):
    return f"{REVERSE_RANKS[card[0]]}{card[1]}"


def cards_to_string(cards):
    return " ".join(card_to_string(card) for card in cards)


def rank_name(rank):
    names = {
        14: "Ace",
        13: "King",
        12: "Queen",
        11: "Jack",
        10: "Ten",
        9: "Nine",
        8: "Eight",
        7: "Seven",
        6: "Six",
        5: "Five",
        4: "Four",
        3: "Three",
        2: "Two"
    }

    return names[rank]


# Validation


def validate_unique_cards(hole_cards, board_cards):
    all_cards = hole_cards + board_cards

    if len(all_cards) != len(set(all_cards)):
        raise ValueError("Duplicate cards detected.")


# Straight Detection


def is_straight(ranks):
    unique = sorted(set(ranks))

    if len(unique) < 5:
        return False, None

    for i in range(len(unique) - 4):

        window = unique[i:i + 5]

        if window == list(range(window[0], window[0] + 5)):
            return True, window[-1]

    # Wheel straight
    if {14, 2, 3, 4, 5}.issubset(unique):
        return True, 5

    return False, None


# Section 2 - Hand Evaluator


import itertools

# Hand Names


HAND_NAMES = {
    9: "Straight Flush",
    8: "Four of a Kind",
    7: "Full House",
    6: "Flush",
    5: "Straight",
    4: "Three of a Kind",
    3: "Two Pair",
    2: "One Pair",
    1: "High Card"
}


# Classify exactly 5 cards


def classify_hand(cards):
    ranks = sorted([c[0] for c in cards], reverse=True)
    suits = [c[1] for c in cards]

    # Count ranks
    counts = {}
    for r in ranks:
        counts[r] = counts.get(r, 0) + 1

    sorted_counts = sorted(
        counts.items(),
        key=lambda x: (-x[1], -x[0])
    )

    # Flush check

    flush_suit = None
    for s in VALID_SUITS:
        if suits.count(s) >= 5:
            flush_suit = s
            break

    # Straight check

    straight, straight_high = is_straight(ranks)

    # Straight Flush

    if flush_suit:
        flush_cards = [c for c in cards if c[1] == flush_suit]
        flush_ranks = sorted([c[0] for c in flush_cards], reverse=True)

        sf, sf_high = is_straight(flush_ranks)

        if sf:
            return {
                "score": (9, sf_high),
                "category": 9,
                "name": HAND_NAMES[9]
            }

    # Four of a Kind

    if sorted_counts[0][1] == 4:
        quad = sorted_counts[0][0]
        kicker = max(r for r in ranks if r != quad)

        return {
            "score": (8, quad, kicker),
            "category": 8,
            "name": HAND_NAMES[8]
        }

    # Full House

    if sorted_counts[0][1] == 3 and sorted_counts[1][1] >= 2:
        return {
            "score": (
                7,
                sorted_counts[0][0],
                sorted_counts[1][0]
            ),
            "category": 7,
            "name": HAND_NAMES[7]
        }

    # Flush

    if flush_suit:
        flush_ranks = sorted(
            [c[0] for c in cards if c[1] == flush_suit],
            reverse=True
        )

        return {
            "score": (6, flush_ranks[:5]),
            "category": 6,
            "name": HAND_NAMES[6]
        }

    # Straight

    if straight:
        return {
            "score": (5, straight_high),
            "category": 5,
            "name": HAND_NAMES[5]
        }

    # Three of a Kind

    if sorted_counts[0][1] == 3:
        trips = sorted_counts[0][0]

        kickers = [r for r in ranks if r != trips][:2]

        return {
            "score": (4, trips, kickers),
            "category": 4,
            "name": HAND_NAMES[4]
        }

    # Two Pair

    if sorted_counts[0][1] == 2 and sorted_counts[1][1] == 2:
        high_pair = sorted_counts[0][0]
        low_pair = sorted_counts[1][0]

        kicker = max(r for r in ranks if r not in (high_pair, low_pair))

        return {
            "score": (3, high_pair, low_pair, kicker),
            "category": 3,
            "name": HAND_NAMES[3]
        }

    # One Pair

    if sorted_counts[0][1] == 2:
        pair = sorted_counts[0][0]

        kickers = [r for r in ranks if r != pair][:3]

        return {
            "score": (2, pair, kickers),
            "category": 2,
            "name": HAND_NAMES[2]
        }

    # High Card

    return {
        "score": (1, ranks[:5]),
        "category": 1,
        "name": HAND_NAMES[1]
    }


# Best 5-card hand from up to 7 cards


# Section 2.5 - Preflop Analyzer


# Hand Category

PREMIUM_PAIRS = {14, 13, 12}  # AA KK QQ
STRONG_PAIRS = {11, 10, 9, 8, 7}  # JJ-TT-99-88-77


def analyze_preflop(hole_cards):
    r1, s1 = hole_cards[0]
    r2, s2 = hole_cards[1]

    high = max(r1, r2)
    low = min(r1, r2)

    suited = (s1 == s2)
    pair = (r1 == r2)

    gap = high - low

    broadway = (high >= 10 and low >= 10)

    ace = (14 in (r1, r2))

    connector = (gap == 1)

    one_gap = (gap == 2)

    analysis = {
        "preflop": None,

        "pair": pair,

        "pair_rank": high if pair else None,

        "suited": suited,

        "connector": connector,

        "one_gap": one_gap,

        "broadway": broadway,

        "ace": ace,

        "category": None,

        "recommendation": None,

        "raise_size": None,

        "reason": []

    }

    # Premium

    if pair and high in PREMIUM_PAIRS:
        analysis["category"] = "Premium"

        analysis["recommendation"] = "Raise"

        analysis["raise_size"] = "3 BB"

        analysis["reason"].append("Premium pocket pair.")

        return analysis

    if suited and ace and low >= 11:
        analysis["category"] = "Premium"

        analysis["recommendation"] = "Raise"

        analysis["raise_size"] = "3 BB"

        analysis["reason"].append("Premium suited Broadway.")

        return analysis

    # Strong

    if pair and high in STRONG_PAIRS:
        analysis["category"] = "Strong"

        analysis["recommendation"] = "Raise"

        analysis["raise_size"] = "3 BB"

        analysis["reason"].append("Strong pocket pair.")

        return analysis

    if broadway:
        analysis["category"] = "Strong"

        analysis["recommendation"] = "Raise"

        analysis["raise_size"] = "2.5 BB"

        analysis["reason"].append("Broadway hand.")

        return analysis

    # Speculative

    if suited and connector:
        analysis["category"] = "Speculative"

        analysis["recommendation"] = "Call"

        analysis["reason"].append("Suited connector.")

        return analysis

    if pair:
        analysis["category"] = "Speculative"

        analysis["recommendation"] = "Call"

        analysis["reason"].append("Small pocket pair.")

        return analysis

    if suited and ace:
        analysis["category"] = "Speculative"

        analysis["recommendation"] = "Call"

        analysis["reason"].append("Suited Ace.")

        return analysis

    # Weak

    analysis["category"] = "Weak"

    analysis["recommendation"] = "Fold"

    analysis["reason"].append("Low equity starting hand.")

    return analysis


def best_hand(hole_cards, board_cards):
    """
    Finds best possible 5-card hand.
    """

    all_cards = hole_cards + board_cards

    if len(all_cards) < 5:
        raise ValueError("Need at least 5 cards")

    best = None

    for combo in itertools.combinations(all_cards, 5):

        result = classify_hand(combo)

        if best is None or result["score"] > best["score"]:
            best = result

    return best


# Flush Draw


def detect_flush_draw(cards):
    suits = {}

    for _, suit in cards:
        suits[suit] = suits.get(suit, 0) + 1

    return max(suits.values()) == 4


# Open Ended Straight Draw


def detect_open_ended_draw(cards):
    ranks = sorted(set(card[0] for card in cards))

    if len(ranks) < 4:
        return False

    for combo in itertools.combinations(ranks, 4):

        combo = sorted(combo)

        if combo == list(range(combo[0], combo[0] + 4)):
            return True

    # Wheel draw
    if {14, 2, 3, 4}.issubset(ranks):
        return True

    return False


# Gutshot


def detect_gutshot(cards):
    ranks = sorted(set(card[0] for card in cards))

    if len(ranks) < 4:
        return False

    for combo in itertools.combinations(ranks, 4):

        low = min(combo)
        high = max(combo)

        if high - low != 4:
            continue

        if len(combo) == 4:
            return True

    return False


# Double Gutshot


def detect_double_gutshot(cards):
    ranks = set(card[0] for card in cards)

    outs = 0

    for candidate in range(2, 15):

        test = sorted(ranks | {candidate})

        straight, _ = is_straight(test)

        if straight:
            outs += 1

    return outs >= 2


# Overcards


def detect_overcards(hole_cards, board_cards):
    if not board_cards:
        return 0

    highest_board = max(card[0] for card in board_cards)

    count = 0

    for rank, _ in hole_cards:

        if rank > highest_board:
            count += 1

    return count


# Combo Draw


def detect_combo_draw(cards):
    flush = detect_flush_draw(cards)

    straight = (
            detect_open_ended_draw(cards)
            or
            detect_gutshot(cards)
    )

    return flush and straight


# Main Draw Analysis


def analyze_draws(hole_cards, board_cards):
    all_cards = hole_cards + board_cards

    flush = detect_flush_draw(all_cards)

    open_draw = detect_open_ended_draw(all_cards)

    gutshot = detect_gutshot(all_cards)

    combo = detect_combo_draw(all_cards)

    overcards = detect_overcards(
        hole_cards,
        board_cards
    )

    return {

        "flush_draw": flush,

        "open_ended": open_draw,

        "gutshot": gutshot,

        "double_gutshot": detect_double_gutshot(all_cards),

        "combo_draw": combo,

        "overcards": overcards

    }


# Determine Current Street

def determine_stage(board_cards):
    board_size = len(board_cards)

    if board_size == 0:
        return "Preflop"

    if board_size == 3:
        return "Flop"

    if board_size == 4:
        return "Turn"

    if board_size == 5:
        return "River"

    return "Unknown"


# Main Hand Analysis


def analyze_hand(hole_cards, board_cards):
    validate_unique_cards(hole_cards, board_cards)

    stage = determine_stage(board_cards)

    analysis = {

        # Game State

        "stage": stage,

        "hole_cards": hole_cards,

        "board_cards": board_cards,

        "all_cards": hole_cards + board_cards,

        # Filled in below

        "position": None,

        "hand": None,

        "draws": None,

        "board": {},

        "pair": {},

        "recommendation": None,

        "reason": None,

        "confidence": None

    }

    # Preflop

    if stage == "Preflop":
        analysis["preflop"] = analyze_preflop(hole_cards)

        return analysis

    # Postflop

    analysis["hand"] = best_hand(
        hole_cards,
        board_cards
    )

    analysis["draws"] = analyze_draws(
        hole_cards,
        board_cards
    )

    return analysis


# Section 5 - Board Analyzer


from collections import Counter


# Flush Texture


def board_flush_texture(board_cards):
    if len(board_cards) < 3:
        return "Unknown"

    suits = [card[1] for card in board_cards]

    counts = Counter(suits)

    highest = max(counts.values())

    if highest >= 4:
        return "Monotone"

    if highest == 3:

        # Flop:
        # H H H

        if len(board_cards) == 3:
            return "Monotone"

        # Turn:
        # H H H C

        return "Monotone"

    if highest == 2:
        return "Two-Tone"

    return "Rainbow"


# Paired Board


def board_is_paired(board_cards):
    ranks = [card[0] for card in board_cards]

    counts = Counter(ranks)

    return any(v >= 2 for v in counts.values())


# Straight Pressure (NEW)


def board_straight_pressure(board_cards):
    ranks = sorted(set(card[0] for card in board_cards))

    if len(ranks) < 3:
        return 0

    pressure = 0

    # Try every possible 5-card straight window
    for start in range(2, 11):  # 2 to 10

        window = set(range(start, start + 5))

        overlap = len(window.intersection(ranks))

        if overlap >= 4:
            pressure += 2  # open-ended / strong draw board
        elif overlap == 3:
            pressure += 1  # gutshot-heavy board

    # Wheel straight special case (A-2-3-4-5)
    wheel = {14, 2, 3, 4, 5}

    if len(wheel.intersection(ranks)) >= 4:
        pressure += 2

    return pressure


def board_straight_texture(board_cards):
    pressure = board_straight_pressure(board_cards)

    if pressure >= 4:
        return "Very Wet"

    if pressure >= 2:
        return "Wet"

    if pressure == 1:
        return "Semi-Wet"

    return "Dry"


# Broadway Presence


def board_broadway_cards(board_cards):
    count = 0

    for rank, _ in board_cards:

        if rank >= 10:
            count += 1

    return count


# Board Danger


def board_danger(board_cards):
    score = 0

    texture = board_straight_texture(board_cards)

    flush = board_flush_texture(board_cards)

    paired = board_is_paired(board_cards)

    broadway = board_broadway_cards(board_cards)

    if texture == "Wet":
        score += 2

    elif texture == "Semi-Wet":
        score += 1

    if flush == "Two-Tone":
        score += 1

    if flush == "Monotone":
        score += 2

    if paired:
        score += 1

    if broadway >= 2:
        score += 1

    if score <= 1:
        return "Low"

    if score <= 3:
        return "Medium"

    return "High"


# Main Board Analysis


def analyze_board(analysis):
    board = analysis["board_cards"]

    analysis["board"] = {

        "flush_texture": board_flush_texture(board),

        "straight_texture": board_straight_texture(board),

        "paired": board_is_paired(board),

        "broadway_cards": board_broadway_cards(board),

        "danger": board_danger(board)

    }

    return analysis


# Section 6 - Pair Analyzer


# Kicker Strength


def kicker_strength(hole_cards):
    ranks = sorted([r for r, _ in hole_cards], reverse=True)

    highest = ranks[0]

    if highest >= 13:
        return "Top"

    if highest >= 10:
        return "Good"

    return "Weak"


# Pair Classification


def pair_quality(hole_cards, board_cards, hand):
    if hand["category"] != 2:
        return {
            "type": hand["name"],
            "kicker": None
        }

    hole_ranks = sorted([r for r, _ in hole_cards], reverse=True)
    board_ranks = sorted([r for r, _ in board_cards], reverse=True)

    highest_board = board_ranks[0]

    pair_rank = hand["score"][1]

    # Pocket Pair Cases

    if hole_ranks[0] == hole_ranks[1]:

        pocket = hole_ranks[0]

        if pocket > highest_board:
            return {
                "type": "Overpair",
                "kicker": None
            }

        if pocket < highest_board:
            return {
                "type": "Underpair",
                "kicker": None
            }

    # One card paired board

    unique_board = sorted(set(board_ranks), reverse=True)

    if pair_rank == unique_board[0]:
        return {
            "type": "Top Pair",
            "kicker": kicker_strength(hole_cards)
        }

    if len(unique_board) >= 2 and pair_rank == unique_board[1]:
        return {
            "type": "Middle Pair",
            "kicker": kicker_strength(hole_cards)
        }

    if pair_rank == unique_board[-1]:
        return {
            "type": "Bottom Pair",
            "kicker": kicker_strength(hole_cards)
        }

    return {
        "type": "One Pair",
        "kicker": kicker_strength(hole_cards)
    }


# Main Pair Analysis


def analyze_pairs(analysis):
    analysis["pair"] = pair_quality(
        analysis["hole_cards"],
        analysis["board_cards"],
        analysis["hand"]
    )

    return analysis


# Section 7 - Position Analyzer


POSITIONS = [
    "UTG",
    "UTG+1",
    "MP",
    "LJ",
    "HJ",
    "CO",
    "BTN",
    "SB",
    "BB"
]

POSITION_STRENGTH = {
    "UTG": 0,
    "UTG+1": 1,
    "MP": 2,
    "LJ": 3,
    "HJ": 4,
    "CO": 5,
    "BTN": 6,
    "SB": 3,
    "BB": 2
}


def determine_position(num_players, seat):
    if seat < 1 or seat > num_players:
        raise ValueError("Invalid seat number.")

    # Heads-up
    if num_players == 2:

        if seat == 1:
            return "SB"

        return "BB"

    # 3-handed
    if num_players == 3:
        mapping = {
            1: "BTN",
            2: "SB",
            3: "BB"
        }

        return mapping[seat]

    # 4-handed
    if num_players == 4:
        mapping = {
            1: "CO",
            2: "BTN",
            3: "SB",
            4: "BB"
        }

        return mapping[seat]

    # 5-handed
    if num_players == 5:
        mapping = {
            1: "HJ",
            2: "CO",
            3: "BTN",
            4: "SB",
            5: "BB"
        }

        return mapping[seat]

    # 6-handed
    if num_players == 6:
        mapping = {
            1: "UTG",
            2: "HJ",
            3: "CO",
            4: "BTN",
            5: "SB",
            6: "BB"
        }

        return mapping[seat]

    # 7-handed
    if num_players == 7:
        mapping = {
            1: "UTG",
            2: "MP",
            3: "HJ",
            4: "CO",
            5: "BTN",
            6: "SB",
            7: "BB"
        }

        return mapping[seat]

    # 8-handed
    if num_players == 8:
        mapping = {
            1: "UTG",
            2: "UTG+1",
            3: "MP",
            4: "HJ",
            5: "CO",
            6: "BTN",
            7: "SB",
            8: "BB"
        }

        return mapping[seat]

    # 9-handed
    mapping = {
        1: "UTG",
        2: "UTG+1",
        3: "MP",
        4: "LJ",
        5: "HJ",
        6: "CO",
        7: "BTN",
        8: "SB",
        9: "BB"
    }

    return mapping[seat]


POSITION_GROUP = {

    "UTG": "Early",
    "UTG+1": "Early",

    "MP": "Middle",
    "LJ": "Middle",
    "HJ": "Middle",

    "CO": "Late",
    "BTN": "Late",

    "SB": "Blind",
    "BB": "Blind"

}


def analyze_position(num_players, seat):
    position = determine_position(num_players, seat)

    return {

        "players": num_players,

        "seat": seat,

        "position": position,

        "group": POSITION_GROUP[position]

    }


# Section 8 - Decision Engine


# Confidence Helper


def determine_confidence(score):
    if score >= 8:
        return "High"

    if score >= 5:
        return "Medium"

    return "Low"


# Main Decision Engine
# Bet Sizing

def recommend_bet_size(action, analysis, pot_size):
    """
    Recommends a bet size based on hand strength,
    board texture, and current pot size.

    Returns:
        float | None
    """

    if action in ("Fold", "Check", "Check/Call"):
        return None

    hand = analysis["hand"]
    board = analysis["board"]

    category = hand["category"]
    danger = board["danger"]

    # Monster hands

    if category >= 7:
        return round(pot_size * 1.00, 2)

    # Strong hands

    if category in (5, 6):

        if danger == "High":
            return round(pot_size * 0.75, 2)

        return round(pot_size * 0.60, 2)

    # Trips

    if category == 4:
        return round(pot_size * 0.65, 2)

    # Top Pair / Overpair

    if category == 2:

        pair_type = analysis["pair"]["type"]

        if pair_type == "Overpair":
            return round(pot_size * 0.70, 2)

        if pair_type == "Top Pair":
            return round(pot_size * 0.60, 2)

        if pair_type == "Middle Pair":
            return round(pot_size * 0.40, 2)

    # Semi-bluffs

    if action == "Semi-Bluff Bet":
        return round(pot_size * 0.50, 2)

    # Default

    return round(pot_size * 0.50, 2)


def recommend_action(analysis, pot_size):
    position = analysis["position"]
    hand = analysis["hand"]
    pair = analysis["pair"]
    draws = analysis["draws"]
    board = analysis["board"]

    score = 0
    reasons = []

    if position["group"] == "Late":

        score += 2
        reasons.append("Late position advantage.")

    elif position["group"] == "Middle":

        score += 1
        reasons.append("Middle position.")

    else:

        reasons.append("Early position.")

    # Made Hands

    if hand["category"] >= 7:

        score += 10
        reasons.append("Very strong made hand.")

    elif hand["category"] == 6:

        score += 8
        reasons.append("Flush.")

    elif hand["category"] == 5:

        score += 8
        reasons.append("Straight.")

    elif hand["category"] == 4:

        score += 7
        reasons.append("Three of a kind.")



    # Pair Strength

    elif hand["category"] == 2:

        pair_type = pair["type"]

        if pair_type == "Overpair":

            score += 7
            reasons.append("Overpair.")

        elif pair_type == "Top Pair":

            score += 6
            reasons.append("Top Pair.")

            kicker = pair["kicker"]

            if kicker == "Top":

                score += 2
                reasons.append("Top kicker.")

            elif kicker == "Good":

                score += 1
                reasons.append("Good kicker.")

        elif pair_type == "Middle Pair":

            score += 4
            reasons.append("Middle pair.")

        elif pair_type == "Bottom Pair":

            score += 2
            reasons.append("Bottom pair.")

        elif pair_type == "Underpair":

            score += 1
            reasons.append("Underpair.")

    # Draws

    if draws["combo_draw"]:

        score += 4
        reasons.append("Combo draw.")

    elif draws["flush_draw"]:

        score += 3
        reasons.append("Flush draw.")

    elif draws["open_ended"]:

        score += 3
        reasons.append("Open-ended straight draw.")

    elif draws["gutshot"]:

        score += 1
        reasons.append("Gutshot straight draw.")

    if draws["overcards"] == 2:
        score += 1
        reasons.append("Two overcards.")

    # Board Danger

    if board["danger"] == "High":

        score -= 2
        reasons.append("Dangerous board.")

    elif board["danger"] == "Medium":

        score -= 1

    # Final Recommendation

    if score >= 10:

        action = "Bet/Raise"

    elif score >= 7:

        action = "Bet"

    elif score >= 5:

        if draws["combo_draw"]:

            action = "Semi-Bluff Bet"

        else:

            action = "Check/Call"

    elif score >= 3:

        action = "Check"

    else:

        action = "Fold"

    analysis["recommendation"] = {
        "action": action,
        "bet_size": None
    }

    analysis["recommendation"] = {
        "action": action,
        "bet_size": recommend_bet_size(action, analysis, pot_size)
    }

    analysis["reason"] = reasons
    analysis["confidence"] = determine_confidence(score)

    return analysis


# Section 8 - Main Program


def display_analysis(analysis):
    if analysis.get("position"):
        print(
            f"Position: {analysis['position']['position']} "
            f"({analysis['position']['group']})"
        )
    if analysis["stage"] == "Preflop":
        pre = analysis["preflop"]

        print("Stage: Preflop")

        print(f"Category: {pre['category']}")
        print(f"Recommendation: {pre['recommendation']}")

        if pre["raise_size"]:
            print(f"Raise Size: {pre['raise_size']}")

        print("\nReasons:")
        for reason in pre["reason"]:
            print(f" • {reason}")

        return
    print(f"Stage: {analysis['stage']}")

    # Hand
    if analysis["hand"] is not None:
        print(f"Best Hand: {analysis['hand']['name']}")

    # Pair
    if analysis["pair"]:
        if analysis["pair"].get("type") not in (None, analysis["hand"]["name"]):
            print(f"Pair Quality: {analysis['pair']['type']}")

        if analysis["pair"].get("kicker"):
            print(f"Kicker: {analysis['pair']['kicker']}")

    # Draws
    draws = analysis["draws"]

    if draws:

        active_draws = []

        if draws["flush_draw"]:
            active_draws.append("Flush Draw")

        if draws["open_ended"]:
            active_draws.append("Open-ended Straight Draw")

        if draws["gutshot"]:
            active_draws.append("Gutshot")

        if draws["double_gutshot"]:
            active_draws.append("Double Gutshot")

        if draws["combo_draw"]:
            active_draws.append("Combo Draw")

        if draws["overcards"] == 2:
            active_draws.append("Two Overcards")
        elif draws["overcards"] == 1:
            active_draws.append("One Overcard")

        if active_draws:
            print("Draws:", ", ".join(active_draws))
        else:
            print("Draws: None")

    # Board
    board = analysis["board"]

    if board:
        print(f"Board Texture: {board['straight_texture']}")
        print(f"Flush Texture: {board['flush_texture']}")
        print(f"Board Danger: {board['danger']}")

    # Recommendation

    rec = analysis["recommendation"]

    print("\nRecommendation:", rec["action"])

    if rec["bet_size"] is not None:
        print(f"Suggested Bet Size: ${rec['bet_size']:.2f}")

    print("Confidence:", analysis["confidence"])

    if analysis["reason"]:
        print("\nReasons:")

        for reason in analysis["reason"]:
            print(" •", reason)


# Evaluate One Stage


def evaluate_stage(hole_cards, board_cards, num_players, seat, pot_size=None):
    analysis = analyze_hand(
        hole_cards,
        board_cards
    )

    analysis["position"] = analyze_position(
        num_players,
        seat
    )
    if analysis["stage"] == "Preflop":
        return analysis

    analysis = analyze_board(analysis)
    analysis = analyze_pairs(analysis)
    analysis = recommend_action(analysis, pot_size)

    return analysis


# Main


def main():
    print("Texas Hold'em Decision Assistant")

    # Position

    players = int(input("\nNumber of players at the table (2-9): "))

    seat = int(input(
        "Your seat order (1 = first to act preflop): "
    ))

    # Preflop

    hole = input(
        "\nEnter your hole cards (example: AS KH): "
    ).split()

    hole_cards = [parse_card(card) for card in hole]

    analysis = evaluate_stage(hole_cards, [], players, seat)
    display_analysis(analysis)

    # Flop

    flop = input(
        "\nEnter the flop (3 cards): "
    ).split()

    flop_cards = [parse_card(card) for card in flop]

    pot_size = float(input("\nCurrent pot size: $"))

    analysis = evaluate_stage(
        hole_cards,
        flop_cards,
        players,
        seat,
        pot_size
    )

    display_analysis(analysis)

    # Turn

    turn = input(
        "\nEnter the turn card: "
    ).split()

    turn_cards = [parse_card(card) for card in turn]

    board = flop_cards + turn_cards

    pot_size = float(input("\nCurrent pot size: $"))

    analysis = evaluate_stage(
        hole_cards,
        board,
        players,
        seat,
        pot_size
    )

    display_analysis(analysis)

    # River

    river = input(
        "\nEnter the river card: "
    ).split()

    river_cards = [parse_card(card) for card in river]

    board += river_cards

    pot_size = float(input("\nCurrent pot size: $"))

    analysis = evaluate_stage(
        hole_cards,
        board,
        players,
        seat,
        pot_size
    )

    display_analysis(analysis)


# Run Program


if __name__ == "__main__":
    main()