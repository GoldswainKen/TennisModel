## calculates probability of winning a tennis match from any given score dependent on the skill levels
## of the two players
 
from game_probability import game_prob
from set_probability import set_general
from tiebreak_probability import tiebreak_prob
 
def fact(x):
    if x in [0, 1]:  return 1
    r = 1
    for a in range(1, (x+1)):  r = r*a
    return r
 
def ch(a, b):
    return fact(a)/(fact(b)*fact(a-b))
 
def match_general(e, v=0, w=0, s=3):
    ## calculates probability of winning the match
    ## from the beginning of a set
    ## e is p(winning a set)
    ## v and w is current set score
    ## s is total number of sets ("best of")
    towin = (s+1)/2
    left = towin - v
    if left == 0:   return 1
    remain = s - v - w
    if left > remain:   return 0
    win = 0
    for i in range(left, (remain+1)):
        add = ch((i-1), (left-1))*(e**(left-1))*((1-e)**(i-left))*e
        win += add
    return win
 
def match_prob(s, t, gv=0, gw=0, sv=0, sw=0, mv=0, mw=0, sets=3):
    ## calculates probability of winning a match from any given score,
    ## given:
    ## s, t: p(server wins a service point), p(server wins return point)
    ## gv, gw: current score within the game. e.g. 30-15 is 2, 1
    ## sv, sw: current score within the set. e.g. 5, 4
    ## mv, mw: current score within the match (number of sets for each player)
    ## v's are serving player; w's are returning player
    ## sets: "best of", so default is best of 3
    a = game_prob(s)
    b = game_prob(t)
    c = set_general(s, t)
    if gv == 0 and gw == 0: ## no point score
        if sv == 0 and sw == 0: ## no game score
            return match_general(c, v=mv, w=mw, s=sets)
        else:   ## we're in mid-set, no point score
            sWin = set_general(a, b, s, t, v=sv, w=sw)
            sLoss = 1 - sWin
    elif sv == 6 and sw == 6:         
        sWin = tiebreak_prob(s, t, v=gv, w=gw)
        sLoss = 1 - sWin       
    else:
        gWin = game_prob(s, v=gv, w=gw)
        gLoss = 1 - gWin
        sWin = gWin*(1 - set_general((1-b), (1-a), (1-t), (1-s), v=sw, w=(sv+1)))
        sWin += gLoss*(1 - set_general((1-b), (1-a), (1-t), (1-s), v=(sw+1), w=sv))
        sLoss = 1 - sWin
    mWin = sWin*match_general(c, v=(mv+1), w=mw, s=sets)
    mWin += sLoss*match_general(c, v=mv, w=(mw+1), s=sets)
    return mWin