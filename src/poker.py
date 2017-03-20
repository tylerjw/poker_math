import pydealer
from pydealer.const import POKER_RANKS
from pprint import pprint

def rank(card):
    return POKER_RANKS['values'][card.value]

def high_card(stack):
    if len(stack) == 0:
        return None
    result = stack[0]
    if len(stack) == 1:
        return result
    for card in stack[1:]:
        if rank(result) < rank(card):
            result = card
    return result

def groups_sort(stack):
    stack.sort()
    groups = []
    current = [stack[0]]
    distance = 0
    for card in stack[1:]:
        distance = abs(rank(card)-rank(current[-1]))
        if distance == 0: 
            current.append(card)
        else:
            groups.append(current)
            current = [card]

    groups.append(current)
    return groups

def build_groups(stack, size=2):
    groups = groups_sort(stack)
    test = lambda l: len(l)==size
    groups = [g for g in groups if test(g)]
    if len(groups)==0:
        groups = None
    return groups

def pairs(stack):
    return build_groups(stack, size=2)

def sets(stack):
    return build_groups(stack, size=3)

def fours(stack):
    return build_groups(stack, size=4)

def two_pair(stack):
    result = pairs(stack)
    if result and len(result) < 2:
        result = None
    return result

def full_house(stack):
    s = sets(stack)
    p = pairs(stack)

    if s and p:
        return s + p
    else:
        return None

def straight_sort(stack):
    if len(stack) < 2:
        return [stack[0]]
    stack.sort()
    straights = []
    current = [stack[0]]
    distance = 0
    for card in stack[1:]:
        distance = abs(rank(card)-rank(current[-1]))
        if distance == 0: 
            continue
        elif distance == 1:
            current.append(card)
        elif distance > 1:
            straights.append(current)
            current = [card]

    straights.append(current)
    return straights

def straight(stack, oesd=False):
    test = None
    if oesd: test = lambda l : l == 4
    else: test = lambda l : l >= 5

    # build the straight sets
    card_lists = straight_sort(stack)
    result = [s for s in card_lists if test(len(s))]
    if len(result) == 0:
        result = None
    return result
    
def oesd(stack):
    return straight(stack, oesd=True)

def hole_draw(stack):
    card_lists = straight_sort(stack)
    if len(card_lists) < 2:
        return None

    tests = [lambda l,r: abs(rank(l[-1])-rank(r[0]))==2, lambda l,r: len(l)+len(r)>=4]

    result = None
    for l,r in zip(card_lists[:-1],card_lists[1:]):
        if tests[0](l,r) and tests[1](l,r):
            result = [l,r]
            break

    return result

def count_suits(stack):
    counts = {}
    for suit in pydealer.SUITS:
        counts[suit] = len(stack.find(suit))
    return counts

def flush(stack, draw=False):
    test = None
    if draw: test = lambda n : n == 4
    else: test = lambda n : n >= 5
    counts = count_suits(stack)
    suit = [s for s in pydealer.SUITS if test(counts[s])]
    if len(suit) == 0: suit = None
    else: suit = suit[0]
    return suit

def flush_draw(stack):
    return flush(stack, draw=True)

def straight_flush(stack):
    suit = flush(stack)
    result = None
    if suit:
        f = [stack[i] for i in stack.find(suit)]
        pprint(f)
        result = straight(f)
    return result

def new_deck():
    deck = pydealer.Deck(ranks=POKER_RANKS)
    deck.shuffle()
    return deck

def rank_hand(hand):
    """
    @brief      Rank the hand of 5 cards

    Poker hand order,number of ranks

    fours
    straight flush
    straight
    flush
    set
    two pair
    pair
    
    @param      hand  The hand
    
    @return     the rank, see above
    """
    tests = [fours,straight_flush,straight,flush,
    sets,two_pair,pairs,high_card]
    ranking = 0
    for i,test in enumerate(tests):
        data = test(hand)
        if not data:
            continue
        other = [c for c in hand if c not in data]

        if data:
            # level
            ranking += 100 * (len(tests) - i - 1)
            hc = high_card([].join(data))
            print(hc)
            ranking += 1 * rank(high_card(data))
            if len(other)>0 and test != high_card:
                ranking += 0.01 * rank(high_card(other))
            break

    return ranking

def main():
    # Construct Deck instance, with 52 cards.
    deck = new_deck()

    hand = pydealer.Stack()
    hand.add(deck.deal(2))
    hand.sort()

    table = pydealer.Stack()
    table.add(deck.deal(3))
    table.sort()

    cards = hand+table

    print('Hand: \n{}'.format(hand))
    print('Table: \n{}'.format(table))

    print(count_suits(cards))
    print('Flush: {}'.format(flush(cards)))
    print('Flush Draw: {}'.format(flush_draw(cards)))

    print('Straight: {}'.format(straight(cards)))
    print('Straight Flush: {}'.format(straight_flush(cards)))
    print('Open-Ended Straight Draw: {}'.format(oesd(cards)))
    print('Gut-Shot Hole Draw: {}'.format(hole_draw(cards)))

    print('Pairs: {}'.format(pairs(cards)))
    print('Sets: {}'.format(sets(cards)))
    print('Fours: {}'.format(fours(cards)))
    print('Full House: {}'.format(full_house(cards)))

    print('High Card: {}'.format(high_card(cards)))

    print('Rank: {}'.format(rank_hand(cards)))

if __name__ == '__main__':
    main()
