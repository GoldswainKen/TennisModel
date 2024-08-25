## calculate the probability of server winning a single game, 
## given p(winning single point) and current point score
 
## s = P(Server Winning the point)
## P(server_score, receiver_score) = P(server_score - 1, receiver_score) + P(server_score, receiver_score - 1)
## 
 
from enum import Enum
from typing import List

class GameWinnerEnum(Enum):
    NOT_OVER = 0
    PLAYER = 1
    OPPONENT = 2

class SetServingEnum(Enum):
    PLAYER = 0
    OPPONENT = 1

def is_player_serving_in_set(player_started_serving: bool, player_score: int, opponent_score: int) -> bool:
    number_of_games = player_score + opponent_score
    if number_of_games % 2 == 0:
        return player_started_serving
    else:
        return not player_started_serving
    
def is_player_serving_in_tiebreak(player_started_serving: bool, player_score: int, opponent_score: int) -> bool:
    number_of_games = player_score + opponent_score
    if number_of_games % 2 == 0:
        return player_started_serving
    else:
        return not player_started_serving

def hold_from_deuce(player_probability: float) -> float:
    """Probability server holds from deuce"""
    opponent_probability = 1 - player_probability
    return (player_probability ** 2) / (1 - (2 * player_probability * opponent_probability))

def game_probability_given_game_score(player_probability: float, game_score: List[int] = [0,0]) -> float:
    player_score = game_score[0]
    opponent_score = game_score[1]
    if player_score >= 4 and player_score - opponent_score <= 2:
        return 1
    elif opponent_score >= 4 and opponent_score - player_score <= 2:
        return 0
    elif player_score == 3 and opponent_score == 3:
        return hold_from_deuce(player_probability)
    else:
        opponent_probability = 1 - player_probability
        down = game_probability_given_game_score(player_probability, [player_score, opponent_score + 1]) * opponent_probability
        up = game_probability_given_game_score(player_probability, [player_score + 1, opponent_score]) * player_probability
        return down + up
    
def set_probability_given_set_score(player_started_serving: bool, server_probability: float, returner_probability: float, set_score: List[int] = [0,0]) -> float:
    player_set_score = set_score[0]
    opponent_set_score = set_score[1]
    if player_set_score >= 6 and player_set_score - opponent_set_score <= 2:
        return 1
    elif opponent_set_score >= 6 and opponent_set_score - player_set_score <= 2:
        return 0
    elif player_set_score == 6 and opponent_set_score == 6:
        return tiebreak_probability(player_started_serving, server_probability, returner_probability)
    else:
        if is_player_serving_in_set(player_set_score, opponent_set_score, player_started_serving):
            down = set_probability_given_set_score(player_started_serving, server_probability, returner_probability, [player_set_score, opponent_set_score + 1]) * (1 - server_probability)
            up = set_probability_given_set_score(player_started_serving, server_probability, returner_probability, [player_set_score + 1, opponent_set_score]) * server_probability
        else:
            down = set_probability_given_set_score(player_started_serving, server_probability, returner_probability, [player_set_score, opponent_set_score + 1]) * (1 - returner_probability)
            up = set_probability_given_set_score(player_started_serving, server_probability, returner_probability, [player_set_score + 1, opponent_set_score]) * returner_probability
        return down + up

def tiebreak_probability(player_started_serving: bool, serving_probability: float, returner_probability: float, tiebreak_score: List[int] = [0,0]) -> float:
    player_tiebreak_score = tiebreak_score[0]
    opponent_tiebreak_score = tiebreak_score[1]
    if player_tiebreak_score == 7 and player_tiebreak_score - opponent_tiebreak_score <= 2:
        return 1
    elif opponent_tiebreak_score == 7 and opponent_tiebreak_score - player_tiebreak_score <= 2:
        return 0
    elif player_tiebreak_score == 7 and opponent_tiebreak_score == 7:
        if is_player_serving_in_tiebreak(player_started_serving, player_tiebreak_score, opponent_tiebreak_score):
            numerator = serving_probability * returner_probability * (1 + serving_probability*(1-returner_probability) + returner_probability*(1-serving_probability))
            denominator = (1 - ((serving_probability**2)*((1-returner_probability)**2) + ((1-serving_probability)**2)*(returner_probability**2) + (2*serving_probability*returner_probability*(1-serving_probability)*(1-returner_probability))))
            return numerator / denominator

    else: 
        if is_player_serving_in_tiebreak(player_started_serving, player_tiebreak_score, opponent_tiebreak_score):
            down = tiebreak_probability(player_started_serving, serving_probability, returner_probability, [player_tiebreak_score, opponent_tiebreak_score + 1]) * (1 - serving_probability)
            up = tiebreak_probability(player_started_serving, serving_probability, returner_probability, [player_tiebreak_score, opponent_tiebreak_score + 1]) * serving_probability
        else:
            down = tiebreak_probability(player_started_serving, serving_probability, returner_probability, [player_tiebreak_score, opponent_tiebreak_score + 1]) * (1 - returner_probability)
            up = tiebreak_probability(player_started_serving, serving_probability, returner_probability, [player_tiebreak_score, opponent_tiebreak_score + 1]) * returner_probability
        return down + up

def main():
    serving_probability_1_point = 0.5
    receiving_probability_1_point = 0.45
    serving_probability_1_game = game_probability_given_game_score(serving_probability_1_point)
    receiving_probability_1_game = game_probability_given_game_score(receiving_probability_1_point)
    player_set_probability = set_probability_given_set_score(True, serving_probability_1_game, receiving_probability_1_game)
    print(ps)

main()