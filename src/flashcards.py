import os, random
import readchar
from pprint import pprint

def print_help():
    help_message = 'This is a simple flashcards program that helps you remember important things from the book.  The data for this app is in flashcards.csv.  To show the answer press any key or \'q\' or Ctl-c to exit.'
    print(help_message)

def build_deck(filename = 'resources/flashcards.csv'):
    deck = []

    with open(filename) as file:
        for line in file:
            elements = [s.strip() for s in line.split(',')]

            if len(elements) > 1:
                card = {'front':elements[0],'back':elements[1]}
                if len(elements) > 2:
                    card['reference'] = elements[2]
                else:
                    card['reference'] = 'not specified'
                deck.append(card)

    return deck

def main():
    done_chars = ['q','Q','\x03','\x04']

    os.system('clear')
    print_help()

    deck = build_deck()

    # randomly sort deck
    deck = random.sample(deck,len(deck))

    print('-------------------------------------')
    print('{} cards in the deck, let us begin.'.format(len(deck)))

    for card in deck:
        print('-------------------------------------')
        print(card['front'])
        key = readchar.readkey()
        print(card['back'])
        print(card['reference'])
        
        if key in done_chars:
            pprint(key)
            break


if __name__ == '__main__':
    main()  
