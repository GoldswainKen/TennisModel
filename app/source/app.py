from dataclasses import dataclass
from typing import List

@dataclass
class Player:
    elo_serve: int
    elo_return: int

@dataclass
class Score:
    started_serving: Player
    started_receiving: Player
    score: str

@dataclass
class Match:
    score: Score
    winner: Player
    loser: Player
    score_progression: List[Score]

@dataclass
class Summary:
    player1: Player
    player2: Player
    simulations: int
    player1_win: int
    player2_win: int

def play_match(player1: Player, player2: Player, score: Score) -> Match:
    pass

def play_matches(player1: Player, player2: Player) -> List[Match]:
    pass

def matches_summary(matches: List[Match]) -> Summary:
    pass

def main() -> None:
    player1 = Player(1500, 1500)
    player2 = Player(1500, 1500)

    matches = play_matches(player1, player2)
    summary = matches_summary(matches)

    print(summary)