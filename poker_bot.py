import random
import json
import os
import time
import re
from treys import Card, Deck, Evaluator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Card utilities

FULL_DECK = Deck().cards[:]


def to_treys(card_str):
    return Card.new(card_str)


def to_treys_list(card_strs):
    return [Card.new(c) for c in card_strs]


def from_treys(card_int):
    return Card.int_to_str(card_int)


def from_treys_list(card_ints):
    return [Card.int_to_str(c) for c in card_ints]


def get_deck(exclude=None):
    if exclude is None:
        return list(FULL_DECK)
    exclude_set = set(exclude)
    return [c for c in FULL_DECK if c not in exclude_set]


# Hand evaluator wrappers

_evaluator = Evaluator()


def rank_hand(hole_cards, board_cards):
    return _evaluator.evaluate(board_cards, hole_cards)


def rank_class(rank):
    return _evaluator.get_rank_class(rank)


def class_string(rank):
    return _evaluator.class_to_string(rank_class(rank))


def compare_hands(hole1, hole2, board):
    r1 = rank_hand(hole1, board)
    r2 = rank_hand(hole2, board)
    if r1 < r2:
        return 1
    elif r1 > r2:
        return -1
    return 0


# Position constants

EARLY = "early"
MIDDLE = "middle"
LATE = "late"
BLIND = "blind"

POSITIONS = [EARLY, MIDDLE, LATE, BLIND]


def adjust_win_rate(wr, position):
    if position == LATE:
        return wr / 0.84
    if position == MIDDLE:
        return wr / 0.92
    if position == BLIND:
        return wr / 0.90
    return wr


# Action thresholds

FOLD = "Fold"
CHECK = "Check"
RAISE_HALF = "Raise 1/2 pot"
RAISE_POT = "Raise pot"
RAISE_1_5X = "Raise 1.5x pot"
RAISE_2X = "Raise 2x pot"
ALL_IN = "All-in"

ALL_ACTIONS = [FOLD, CHECK, RAISE_HALF, RAISE_POT, RAISE_1_5X, RAISE_2X, ALL_IN]

STANDARD_THRESHOLDS = [
    (0.85, RAISE_2X),
    (0.70, RAISE_1_5X),
    (0.55, RAISE_POT),
    (0.40, RAISE_HALF),
    (0.25, CHECK),
    (0.00, FOLD),
]


def action_from_win_rate(wr):
    for cutoff, action in STANDARD_THRESHOLDS:
        if wr >= cutoff:
            return action
    return FOLD


def pick_thresholds(position):
    if position == LATE:
        return [
            (0.80, RAISE_2X),
            (0.65, RAISE_1_5X),
            (0.50, RAISE_POT),
            (0.37, RAISE_HALF),
            (0.22, CHECK),
            (0.00, FOLD),
        ]
    return STANDARD_THRESHOLDS


def action_index(action):
    for i, a in enumerate(ALL_ACTIONS):
        if a == action:
            return i
    return 5


def shift_action(action, steps):
    idx = action_index(action)
    new_idx = idx + steps
    if new_idx < 0:
        new_idx = 0
    if new_idx >= len(ALL_ACTIONS):
        new_idx = len(ALL_ACTIONS) - 1
    return ALL_ACTIONS[new_idx]


# Monte Carlo equity simulation


def win_rate(hole_cards, board_cards=None, n_opponents=1, trials=10000):
    if board_cards is None:
        board_cards = []

    known = list(hole_cards) + list(board_cards)
    remaining_deck = get_deck(exclude=known)
    cards_to_deal = 5 - len(board_cards)
    wins = 0
    ties = 0

    for _ in range(trials):
        sampled = random.sample(remaining_deck, cards_to_deal + 2 * n_opponents)

        sim_board = list(board_cards) + sampled[:cards_to_deal]
        our_rank = rank_hand(list(hole_cards), sim_board)

        best_opp_rank = 9999
        idx = cards_to_deal
        for _ in range(n_opponents):
            opp_hole = [sampled[idx], sampled[idx + 1]]
            opp_rank = rank_hand(opp_hole, sim_board)
            if opp_rank < best_opp_rank:
                best_opp_rank = opp_rank
            idx += 2

        if our_rank < best_opp_rank:
            wins += 1
        elif our_rank == best_opp_rank:
            ties += 1

    return (wins + ties * 0.5) / trials


# Hand reading utilities


def get_rank(card_int):
    return Card.get_rank_int(card_int)


def get_suit(card_int):
    return Card.get_suit_int(card_int)


def hand_category(hole, board):
    all_cards = list(hole) + list(board)
    values = [get_rank(c) for c in all_cards]
    suits = [get_suit(c) for c in all_cards]

    rank_counts = {}
    for v in values:
        rank_counts[v] = rank_counts.get(v, 0) + 1

    pairs = 0
    trips = 0
    quads = 0
    for c in rank_counts.values():
        if c == 4:
            quads += 1
        elif c == 3:
            trips += 1
        elif c == 2:
            pairs += 1

    if quads >= 1:
        return "quads"
    if trips >= 1 and pairs >= 1:
        return "full_house"
    if trips >= 1:
        return "trips"
    if pairs == 2:
        return "two_pair"

    hole_vals = [get_rank(h) for h in hole]

    if pairs == 1:
        if hole_vals[0] == hole_vals[1]:
            if hole_vals[0] >= 12:
                return "overpair"
            return "pocket_pair"
        pair_rank = -1
        for r, c in rank_counts.items():
            if c == 2:
                pair_rank = r
                break
        board_ranks = [get_rank(c) for c in board]
        if pair_rank in board_ranks:
            if pair_rank >= 9:
                return "top_pair"
            return "mid_pair"
        return "pair_board"

    suit_counts = {}
    for s in suits:
        suit_counts[s] = suit_counts.get(s, 0) + 1

    flush_draw = False
    for s, cnt in suit_counts.items():
        if cnt == 4:
            flush_draw = True

    unique_vals = sorted(set(values))
    oesd = False
    gutshot = False

    if len(unique_vals) >= 5:
        for i in range(len(unique_vals) - 4):
            if unique_vals[i+4] - unique_vals[i] == 4:
                oesd = True
                break

        if not oesd:
            for i in range(len(unique_vals) - 4):
                gaps = 0
                for j in range(4):
                    if unique_vals[i+j+1] - unique_vals[i+j] != 1:
                        gaps += 1
                if gaps == 1 and unique_vals[i+4] - unique_vals[i] <= 5:
                    gutshot = True
                    break

    if 14 in values:
        if all(v in values for v in [2, 3, 4, 5]):
            oesd = True

    if flush_draw and oesd:
        return "combo_draw"
    if flush_draw:
        return "flush_draw"
    if oesd:
        return "oesd"
    if gutshot:
        return "gutshot"

    return "high_card"


def draw_outs(hole, board):
    all_cards = list(hole) + list(board)
    values = [get_rank(c) for c in all_cards]
    suits = [get_suit(c) for c in all_cards]

    suit_counts = {}
    for s in suits:
        suit_counts[s] = suit_counts.get(s, 0) + 1

    flush_outs = 0
    for s, cnt in suit_counts.items():
        if cnt == 4:
            flush_outs = 9

    straight_outs = 0
    unique = sorted(set(values))
    for out_card in range(2, 15):
        if out_card in values:
            continue
        check = sorted(set(values + [out_card]))
        for i in range(len(check) - 4):
            if check[i+4] - check[i] == 4:
                straight_outs = max(straight_outs, 1)
                if len(check) == len(unique) + 1:
                    straight_outs = 8 if flush_outs == 9 else 4

    draw_type = "none"
    if flush_outs > 0 and straight_outs >= 4:
        draw_type = "combo_draw"
    elif flush_outs > 0:
        draw_type = "flush_draw"
    elif straight_outs >= 8:
        draw_type = "oesd"
    elif straight_outs >= 4:
        draw_type = "gutshot"

    return flush_outs, straight_outs, draw_type


def board_texture(cards):
    if len(cards) == 0:
        return "dry"

    ranks = [get_rank(c) for c in cards]
    suits = [get_suit(c) for c in cards]

    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1

    suit_counts = {}
    for s in suits:
        suit_counts[s] = suit_counts.get(s, 0) + 1

    paired = max(rank_counts.values()) >= 2
    flush_possible = max(suit_counts.values()) >= 3
    monotone = max(suit_counts.values()) == len(cards)

    sorted_ranks = sorted(set(ranks))
    gaps = 0
    for i in range(len(sorted_ranks) - 1):
        if sorted_ranks[i+1] - sorted_ranks[i] > 2:
            gaps += 1

    connected = False
    for i in range(len(sorted_ranks) - 2):
        if sorted_ranks[i+2] - sorted_ranks[i] <= 4:
            connected = True

    high_cards = sum(1 for r in ranks if r >= 11)

    if monotone and connected:
        return "very_wet"
    if flush_possible and connected:
        return "wet"
    if connected and not paired:
        return "semi_wet"
    if paired:
        return "paired"
    if gaps <= 1 and high_cards <= 1:
        return "dry"
    if gaps <= 2:
        return "moderate"
    return "dry"


def texture_bet_mult(texture):
    if texture == "very_wet":
        return 0.5
    if texture == "wet":
        return 0.6
    if texture == "semi_wet":
        return 0.8
    if texture == "paired":
        return 0.9
    if texture == "dry":
        return 1.2
    return 1.0


def implied_odds_mult(draw_type, stack_pot_ratio):
    if draw_type == "combo_draw":
        base = 0.15
    elif draw_type in ("flush_draw", "oesd"):
        base = 0.10
    elif draw_type == "gutshot":
        base = 0.05
    else:
        base = 0.0
    ratio = min(stack_pot_ratio, 20.0) / 10.0
    return base * ratio


# Opponent modeling

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "opponent_db.json")


class OpponentModel:
    def __init__(self, player_id):
        self.player_id = player_id
        self.vpip_opps = 0
        self.vpip_acts = 0
        self.faced_raise = 0
        self.folded_raise = 0
        self.action_opps = 0
        self.raise_acts = 0
        self.agg_actions = 0
        self.pass_actions = 0
        self.hands_shown = []

    def record_preflop_action(self, action):
        self.vpip_opps += 1
        if action in ("call", "raise"):
            self.vpip_acts += 1

    def record_response_to_raise(self, folded):
        self.faced_raise += 1
        if folded:
            self.folded_raise += 1

    def record_action(self, action):
        self.action_opps += 1
        if action == "raise":
            self.raise_acts += 1
            self.agg_actions += 1
        elif action in ("call", "check"):
            self.pass_actions += 1

    def record_showdown(self, hole_cards, won):
        self.hands_shown.append({"cards": hole_cards, "won": won})
        if len(self.hands_shown) > 50:
            self.hands_shown = self.hands_shown[-50:]

    def vpip(self):
        if self.vpip_opps < 10:
            return None
        return self.vpip_acts / self.vpip_opps

    def fold_to_raise(self):
        if self.faced_raise < 10:
            return None
        return self.folded_raise / self.faced_raise

    def confidence(self):
        samples = max(self.vpip_opps, self.faced_raise, self.action_opps)
        if samples >= 50:
            return 1.0
        return samples / 50.0

    def action_adjustment(self):
        adj = 0
        ftr = self.fold_to_raise()
        if ftr is not None:
            if ftr > 0.60:
                adj += 1
            elif ftr < 0.25:
                adj -= 1
        vp = self.vpip()
        if vp is not None:
            if vp < 0.20:
                adj -= 1
            elif vp > 0.50:
                adj += 1
        return adj

    def to_dict(self):
        return {
            "vpip_opps": self.vpip_opps,
            "vpip_acts": self.vpip_acts,
            "faced_raise": self.faced_raise,
            "folded_raise": self.folded_raise,
            "action_opps": self.action_opps,
            "raise_acts": self.raise_acts,
            "agg_actions": self.agg_actions,
            "pass_actions": self.pass_actions,
            "hands_shown": self.hands_shown,
        }

    def from_dict(self, data):
        self.vpip_opps = data.get("vpip_opps", 0)
        self.vpip_acts = data.get("vpip_acts", 0)
        self.faced_raise = data.get("faced_raise", 0)
        self.folded_raise = data.get("folded_raise", 0)
        self.action_opps = data.get("action_opps", 0)
        self.raise_acts = data.get("raise_acts", 0)
        self.agg_actions = data.get("agg_actions", 0)
        self.pass_actions = data.get("pass_actions", 0)
        self.hands_shown = data.get("hands_shown", [])


class OpponentModelRegistry:
    def __init__(self, persist=True):
        self._models = {}
        self._persist = persist
        if persist:
            self._load()

    def get(self, player_id):
        if player_id not in self._models:
            self._models[player_id] = OpponentModel(player_id)
        return self._models[player_id]

    def all_players(self):
        return list(self._models.keys())

    def reset(self):
        self._models = {}

    def _load(self):
        if not os.path.exists(DB_PATH):
            return
        try:
            with open(DB_PATH, "r") as f:
                data = json.load(f)
            for pid, stats in data.items():
                m = OpponentModel(pid)
                m.from_dict(stats)
                self._models[pid] = m
        except (json.JSONDecodeError, IOError):
            pass

    def save(self):
        if not self._persist:
            return
        data = {}
        for pid, model in self._models.items():
            data[pid] = model.to_dict()
        try:
            with open(DB_PATH, "w") as f:
                json.dump(data, f)
        except IOError:
            pass

    def __del__(self):
        if self._persist:
            try:
                self.save()
            except Exception:
                pass


# Baseline bot classes for testing


class AlwaysRaiseBot:
    def decide(self, game_state):
        return RAISE_2X


class AlwaysCallBot:
    def decide(self, game_state):
        return CHECK


class TightFoldBot:
    THRESHOLD = 0.80

    def decide(self, game_state):
        hole = to_treys_list(game_state["hole_cards"])
        board = to_treys_list(game_state.get("board_cards", []))
        n_opp = game_state.get("n_opponents", 1)
        wr = win_rate(hole, board_cards=board, n_opponents=n_opp, trials=4000)
        if wr >= self.THRESHOLD:
            return RAISE_2X
        return FOLD


class RandomBot:
    def decide(self, game_state):
        return random.choice(ALL_ACTIONS)


class StaticWinRateBot:
    def decide(self, game_state):
        hole = to_treys_list(game_state["hole_cards"])
        board = to_treys_list(game_state.get("board_cards", []))
        n_opp = game_state.get("n_opponents", 1)
        wr = win_rate(hole, board_cards=board, n_opponents=n_opp, trials=4000)
        return action_from_win_rate(wr)


# Pre-flop hand ranges by position

RANK_MAP = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
CHAR_MAP = {14: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: 'T', 9: '9', 8: '8',
            7: '7', 6: '6', 5: '5', 4: '4', 3: '3', 2: '2'}


def hand_key(hole_strs):
    r1 = RANK_MAP[hole_strs[0][0].upper()]
    r2 = RANK_MAP[hole_strs[1][0].upper()]
    suited = hole_strs[0][1] == hole_strs[1][1]
    high = max(r1, r2)
    low = min(r1, r2)
    if r1 == r2:
        return CHAR_MAP[high] + CHAR_MAP[high]
    key = CHAR_MAP[high] + CHAR_MAP[low]
    if suited:
        key += 's'
    return key


PREFLOP_RANGES = {
    EARLY: {
        'raise': {'AA', 'KK', 'QQ', 'JJ', 'TT', '99', 'AKs', 'AK', 'AQs',
                  'AQ', 'AJs', 'ATs', 'KQs', 'KQ', 'KJs'},
        'call': {'88', '77', 'AJ', 'AT', 'KTs', 'QJs', 'QTs', 'JTs', 'T9s'},
        '3bet': {'AA', 'KK', 'QQ', 'AKs', 'AK'},
        '3bet_call': {'JJ', 'TT', 'AQs', 'AQ'},
    },
    MIDDLE: {
        'raise': {'AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', 'AKs', 'AK',
                  'AQs', 'AQ', 'AJs', 'AJ', 'ATs', 'KQs', 'KQ', 'KJs',
                  'KTs', 'QJs', 'QTs', 'JTs', 'T9s', 'A9s', 'A8s'},
        'call': {'77', '66', '55', 'AT', 'KJ', 'QJ', 'JT', 'T8s', '98s', '87s'},
        '3bet': {'AA', 'KK', 'QQ', 'JJ', 'AKs', 'AK', 'AQs'},
        '3bet_call': {'TT', '99', 'AQ', 'AJs', 'KQs'},
    },
    LATE: {
        'raise': {'AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55',
                  'AKs', 'AK', 'AQs', 'AQ', 'AJs', 'AJ', 'ATs', 'AT',
                  'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
                  'KQs', 'KQ', 'KJs', 'KTs', 'K9s', 'QJs', 'QTs', 'Q9s',
                  'JTs', 'J9s', 'T9s', 'T8s', '98s', '97s', '87s', '86s', '76s'},
        'call': {'44', '33', '22', 'KJ', 'KT', 'QJ', 'JT', 'K8s', 'Q8s',
                 'J8s', 'T7s', '75s'},
        '3bet': {'AA', 'KK', 'QQ', 'JJ', 'TT', 'AKs', 'AK', 'AQs', 'AQ'},
        '3bet_call': {'99', '88', 'AJs', 'ATs', 'KQs', 'KJs', 'QJs', 'JTs'},
    },
    BLIND: {
        'raise': {'AA', 'KK', 'QQ', 'JJ', 'TT', '99', 'AKs', 'AK', 'AQs',
                  'AQ', 'AJs', 'ATs', 'KQs', 'KQ', 'KJs', 'QJs', 'JTs'},
        'call': {'88', '77', '66', '55', '44', '33', '22', 'AJ', 'AT',
                 'KTs', 'QTs', 'T9s', '98s', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s',
                 'A4s', 'A3s', 'A2s'},
        '3bet': {'AA', 'KK', 'QQ', 'AKs', 'AK', 'AQs'},
        '3bet_call': {'JJ', 'TT', 'AQ', 'AJs', 'KQs'},
    },
}


def preflop_decision(hole_strs, position, facing_raise=False, facing_3bet=False):
    key = hand_key(hole_strs)
    ranges = PREFLOP_RANGES[position]

    if facing_3bet:
        if key in ranges['3bet_call']:
            return CHECK
        if key in ranges['3bet']:
            return RAISE_POT
        return FOLD

    if facing_raise:
        if key in ranges['3bet']:
            return RAISE_2X
        if key in ranges['3bet_call']:
            return CHECK
        if key in ranges['call']:
            return CHECK
        return FOLD

    if key in ranges['raise']:
        return RAISE_POT
    if key in ranges['call']:
        return CHECK
    return FOLD


# Main poker bot class


class PokerBot:
    def __init__(self):
        self.opponent_registry = OpponentModelRegistry(persist=True)
        self.hand_memory = {}
        self.hand_id = 0
        self.mc_trials = 8000
        self.bluff_frequencies = {
            'very_wet': 0.25, 'wet': 0.20, 'semi_wet': 0.15,
            'paired': 0.12, 'moderate': 0.10, 'dry': 0.08,
        }

    def new_hand(self):
        self.hand_id += 1
        self.hand_memory[self.hand_id] = {
            "aggressor": False,
            "cbet": False,
            "cbet_success": False,
            "previous_action": None,
            "street": "preflop",
            "preflop_action": None,
            "facing_raise": False,
        }

    def _hand_strength_class(self, hole, board):
        rank = rank_hand(hole, board)
        cls = rank_class(rank)
        if cls <= 3:
            return "monster"
        if cls <= 5:
            return "strong"
        if cls == 6:
            return "decent"
        return "weak"

    def decide(self, game_state):
        hole_cards = game_state["hole_cards"]
        board_cards = game_state.get("board_cards", [])
        pot = game_state.get("pot", 0)
        stack = game_state.get("stack", 1000)
        to_call = game_state.get("to_call", 0)
        opponent_id = game_state.get("opponent_id", "unknown")
        facing_all_in = game_state.get("facing_all_in", False)
        n_opponents = game_state.get("n_opponents", 1)
        position = game_state.get("position", MIDDLE)
        street = game_state.get("street", "preflop")

        if self.hand_id not in self.hand_memory:
            self.new_hand()
        mem = self.hand_memory[self.hand_id]
        mem["street"] = street

        hole = to_treys_list(hole_cards)
        board = to_treys_list(board_cards) if board_cards else []

        # ---------------------------------------------------------------
        # PREFLOP  —  range-based strategy
        # ---------------------------------------------------------------
        if street == "preflop" and not board_cards:
            if facing_all_in:
                wr = win_rate(hole, board_cards=[], n_opponents=n_opponents, trials=self.mc_trials)
                if wr >= 0.40:
                    return CHECK
                return FOLD

            action = preflop_decision(
                hole_cards, position,
                facing_raise=(to_call > 0),
                facing_3bet=False,
            )
            mem["preflop_action"] = action
            if action != FOLD:
                mem["aggressor"] = (action != CHECK)

            if action == FOLD and to_call == 0:
                return CHECK
            if action == FOLD and to_call > 0:
                pot_odds = to_call / (pot + to_call)
                wr = win_rate(hole, board_cards=[], n_opponents=n_opponents, trials=self.mc_trials)
                if wr > pot_odds:
                    return CHECK
            return action

        # ---------------------------------------------------------------
        # POST-FLOP  —  equity + board-aware strategy
        # ---------------------------------------------------------------
        win_pct = win_rate(hole, board_cards=board, n_opponents=n_opponents, trials=self.mc_trials)
        win_pct = adjust_win_rate(win_pct, position)

        flush_outs, straight_outs, draw_type = draw_outs(hole, board)
        tex = board_texture(board) if board else "dry"
        bet_mult = texture_bet_mult(tex)
        spr = stack / max(pot, 1)
        win_pct += implied_odds_mult(draw_type, spr)

        strength = self._hand_strength_class(hole, board)
        opp_model = self.opponent_registry.get(opponent_id)
        opp_adj = opp_model.action_adjustment()

        # Base action from win rate
        action = action_from_win_rate(win_pct)

        # Opponent adjustment
        if opp_adj != 0:
            action = shift_action(action, opp_adj)

        # Semi-bluff with draws
        if draw_type in ("combo_draw", "flush_draw", "oesd") and win_pct > 0.25:
            bluff_freq = self.bluff_frequencies.get(tex, 0.10)
            if random.random() < bluff_freq:
                action = shift_action(action, 1)

        # Deliberate bluff on favorable board textures
        if strength == "weak":
            bluff_freq = self.bluff_frequencies.get(tex, 0.10)
            blockers = self._has_blockers(hole, board)
            if blockers and random.random() < bluff_freq:
                action = shift_action(action, 1)

        # Continuation bet on favorable flops
        if mem.get("aggressor") and street in ("flop", "turn") and not mem.get("cbet"):
            favorable = self._cbet_favorable(hole, board, tex, strength)
            if favorable and win_pct > 0.25:
                action = shift_action(action, 1)
                mem["cbet"] = True
            elif not favorable and strength in ("weak", "drawing"):
                action = shift_action(action, -1)

        # Bet sizing: bigger value bets on wet boards, smaller bluffs
        if strength in ("monster", "strong") and action in (RAISE_HALF, RAISE_POT, RAISE_1_5X):
            if tex in ("very_wet", "wet"):
                action = shift_action(action, 1)
            elif tex in ("dry", "paired"):
                action = shift_action(action, -1)

        # Pot-odds aware calling
        if action == FOLD and to_call > 0:
            pot_odds = to_call / (pot + to_call)
            if win_pct > pot_odds + 0.02:
                action = CHECK
                mem["pot_odds_call"] = True

        # Randomization for deception
        confidence = opp_model.confidence()
        epsilon = max(0.02, 0.15 * (1.0 - confidence))
        if random.random() < epsilon:
            action = shift_action(action, random.choice([-1, 0, 1]))

        action = self.edge_cases(action, win_pct, pot, stack, to_call, facing_all_in, bet_mult)

        mem["previous_action"] = action
        if action not in (FOLD, CHECK):
            mem["aggressor"] = True

        return action

    def _has_blockers(self, hole, board):
        ranks = sorted([get_rank(c) for c in hole])
        board_ranks = sorted([get_rank(c) for c in board])
        if 14 in ranks and 13 in ranks:
            return True
        if 14 in ranks:
            return any(r == 13 or r == 12 for r in board_ranks)
        return False

    def _cbet_favorable(self, hole, board, tex, strength):
        if strength in ("monster", "strong", "decent"):
            return True
        if strength == "drawing" and tex in ("semi_wet", "dry"):
            return True
        if tex == "dry":
            return True
        if tex == "paired" and strength != "weak":
            return True
        return False

    def record_opponent_action(self, opponent_id, action, context="general"):
        model = self.opponent_registry.get(opponent_id)
        if context == "preflop":
            model.record_preflop_action(action)
        elif context == "facing_raise":
            model.record_response_to_raise(folded=(action == "fold"))
        else:
            model.record_action(action)

    def record_showdown(self, opponent_id, hole_cards, won):
        model = self.opponent_registry.get(opponent_id)
        model.record_showdown(hole_cards, won)

    def new_match(self):
        self.opponent_registry.save()
        self.hand_memory = {}

    def edge_cases(self, action, win_pct, pot, stack, to_call, facing_all_in, bet_mult=1.0):
        if facing_all_in:
            if win_pct >= 0.40:
                return CHECK
            return FOLD

        if action in (RAISE_HALF, RAISE_POT, RAISE_1_5X, RAISE_2X):
            mults = {"Raise 1/2 pot": 0.5, "Raise pot": 1.0, "Raise 1.5x pot": 1.5, "Raise 2x pot": 2.0}
            base_mult = mults.get(action, 1.0)
            raise_amount = int(pot * base_mult * bet_mult)
            if raise_amount > stack:
                if win_pct >= 0.40:
                    return ALL_IN
                if to_call > 0:
                    return FOLD
                return CHECK

        if action == CHECK and to_call > 0:
            pot_odds = to_call / (pot + to_call)
            if win_pct > pot_odds - 0.03:
                return CHECK
            return FOLD

        if to_call == 0 and action == FOLD:
            return CHECK

        return action


# Pre-flop rate function


def rate_preflop(hole_cards, n_opponents=1, trials=10000, position=MIDDLE):
    hole = to_treys_list(hole_cards)
    wr = win_rate(hole, board_cards=[], n_opponents=n_opponents, trials=trials)
    adj_wr = adjust_win_rate(wr, position)
    action = action_from_win_rate(adj_wr)
    return action


# Flop rate function


def rate_flop(hole_cards, board_cards, n_opponents=1, trials=10000, position=MIDDLE):
    if len(board_cards) != 3:
        raise ValueError(f"Flop requires exactly 3 board cards, got {len(board_cards)}")

    hole = to_treys_list(hole_cards)
    board = to_treys_list(board_cards)
    wr = win_rate(hole, board_cards=board, n_opponents=n_opponents, trials=trials)
    adj_wr = adjust_win_rate(wr, position)

    _, _, draw_type = draw_outs(hole, board)
    if draw_type in ("flush_draw", "combo_draw"):
        adj_wr += 0.05

    action = action_from_win_rate(adj_wr)
    return action


# Turn rate function


def rate_turn(hole_cards, board_cards, n_opponents=1, trials=10000, position=MIDDLE):
    if len(board_cards) != 4:
        raise ValueError(f"Turn requires exactly 4 board cards, got {len(board_cards)}")

    hole = to_treys_list(hole_cards)
    board = to_treys_list(board_cards)
    wr = win_rate(hole, board_cards=board, n_opponents=n_opponents, trials=trials)
    adj_wr = adjust_win_rate(wr, position)

    tex = board_texture(board)
    bet_mult = texture_bet_mult(tex)
    adj_wr *= bet_mult

    action = action_from_win_rate(adj_wr)
    return action


# River rate function


def rate_river(hole_cards, board_cards, n_opponents=1, trials=10000, position=MIDDLE):
    if len(board_cards) != 5:
        raise ValueError(f"River requires exactly 5 board cards, got {len(board_cards)}")

    hole = to_treys_list(hole_cards)
    board = to_treys_list(board_cards)
    wr = win_rate(hole, board_cards=board, n_opponents=n_opponents, trials=trials)
    adj_wr = adjust_win_rate(wr, position)

    tex = board_texture(board)
    bet_mult = texture_bet_mult(tex)
    adj_wr *= bet_mult

    action = action_from_win_rate(adj_wr)
    return action


# PokerNow web scanner


class PokerNowScanner:
    def __init__(self, game_url="", player_name="", headless=True):
        self.game_url = game_url
        self.player_name = player_name or "You"
        self.bot = PokerBot()
        self.headless = headless
        self.driver = None
        self.opponent_id = "opponent"

    def connect(self):
        options = webdriver.ChromeOptions()
        if not self.headless:
            options.add_argument("--start-maximized")
        else:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(self.game_url)
        self.wait = WebDriverWait(self.driver, 30)

    def click_sit(self):
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, "button.table-player-seat-button")
            btn.click()
            time.sleep(1)
            print("[Scanner] Clicked SIT")
            return True
        except Exception:
            return False

    def scrape_state(self):
        js = """
        const state = { hole: [], board: [], pot: 0, myTurn: false, buttons: [] };

        const allButtons = document.querySelectorAll('button');
        allButtons.forEach(b => {
            const t = b.textContent.trim().toLowerCase();
            if (t === 'fold' || t === 'check' || t === 'call' || t === 'raise' ||
                t === 'all-in' || t.indexOf('all in') >= 0) {
                state.buttons.push(b.textContent.trim());
                state.myTurn = true;
            }
        });

        const allEls = document.querySelectorAll('*');
        allEls.forEach(el => {
            const tid = (el.getAttribute('data-testid') || '').toLowerCase();
            if (tid.startsWith('card-')) {
                state.hole.push(tid.replace('card-', ''));
            }
        });

        const boardEls = document.querySelectorAll('[class*="board"], [class*="community"], [class*="Board"], [class*="Community"]');
        boardEls.forEach(el => {
            const cards = el.querySelectorAll('[data-testid]');
            cards.forEach(c => {
                const tid = (c.getAttribute('data-testid') || '').toLowerCase();
                if (tid.startsWith('card-')) {
                    state.board.push(tid.replace('card-', ''));
                }
            });
        });

        const body = document.body.textContent;
        const potMatch = body.match(/[Pp]ot[:\u00a0 ]*([0-9,]+)/);
        if (potMatch) state.pot = parseInt(potMatch[1].replace(/,/g, ''));

        return state;
        """
        return self.driver.execute_script(js)

    def convert_card(self, raw):
        raw = raw.strip()
        if len(raw) == 2:
            r, s = raw[0], raw[1].lower()
        elif len(raw) == 3:
            r, s = raw[:2], raw[2].lower()
        else:
            return None
        if r == "10":
            r = "T"
        return f"{r}{s}"

    def convert_cards(self, raw_list):
        seen = set()
        result = []
        for c in raw_list:
            converted = self.convert_card(c)
            if converted and converted not in seen:
                seen.add(converted)
                result.append(converted)
        return result

    def separate_hole_and_board(self, state):
        all_cards = self.convert_cards(state["hole"])
        board = self.convert_cards(state["board"])

        if len(all_cards) <= 2:
            return all_cards, board

        if len(board) >= 3:
            hole = [c for c in all_cards if c not in board]
            if len(hole) >= 2:
                return hole[:2], board

        return all_cards[:2], board

    def get_action(self, hole_cards, board_cards, pot):
        if len(hole_cards) != 2:
            return None
        return self.bot.decide({
            "hole_cards": hole_cards,
            "board_cards": board_cards,
            "pot": pot,
            "stack": 1000,
            "to_call": 0,
            "opponent_id": self.opponent_id,
            "facing_all_in": False,
            "n_opponents": 1,
            "position": MIDDLE,
            "street": {0: "preflop", 3: "flop", 4: "turn", 5: "river"}.get(len(board_cards), "preflop"),
        })

    def click_action(self, action):
        text = action.lower()
        try:
            btn = self.driver.find_element(By.XPATH,
                f"//button[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='{text}']")
            btn.click()
            return True
        except Exception:
            pass
        try:
            btn = self.driver.find_element(By.XPATH,
                f"//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text}')]")
            btn.click()
            return True
        except Exception:
            pass
        return False

    def run(self):
        if not self.driver:
            self.connect()

        print(f"Connected to {self.game_url}")
        time.sleep(2)

        if self.click_sit():
            print("Waiting for hand to begin...")
            time.sleep(3)

        ticks = 0
        while True:
            try:
                state = self.scrape_state()

                if ticks % 10 == 0:
                    print(f"  scanning... buttons={len(state['buttons'])} cards={len(state['hole'])} pot={state['pot']}")

                if state["myTurn"] and len(state["buttons"]) > 0:
                    hole, board = self.separate_hole_and_board(state)
                    pot = state["pot"]

                    if len(hole) == 2:
                        action = self.get_action(hole, board, pot)
                        if action:
                            print(f"\n>>> {action}  |  {hole}  board={board}  pot={pot}")
                            self.click_action(action)
                    else:
                        print(f"  My turn, cards unclear. raw hole={state['hole']} board={state['board']}")

                time.sleep(1)
                ticks += 1
            except KeyboardInterrupt:
                print("\nStopped.")
                break
            except Exception as e:
                print(f"  Error: {e}")
                time.sleep(2)

    def close(self):
        if self.driver:
            self.driver.quit()

    def __del__(self):
        self.close()


def scanner_main():
    import sys
    args = sys.argv[1:]
    url = ""
    player_name = ""
    headless = True

    for a in args:
        if a == "-v":
            headless = False
        elif a.startswith("--player="):
            player_name = a.split("=", 1)[1]
        elif a.startswith("http"):
            url = a
        elif not a.startswith("-"):
            url = a

    if not url:
        url = input("PokerNow game URL: ").strip()
    if not player_name:
        p = input("Your player name (or press Enter to skip): ").strip()
        if p:
            player_name = p

    scanner = PokerNowScanner(game_url=url, player_name=player_name, headless=headless)
    try:
        scanner.run()
    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        scanner.close()