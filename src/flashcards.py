import os

def enter_to_continue():
    enter_message = 'Press enter to continue.'
    __ = input(enter_message)

def wait_for_enter():
    __ = input('')

def print_help():
    help_message = 'This is a simple flashcards system that helps you remember important things from the book.  The data for this app is in flashcards.csv.  To show the answer press enter.'
    print(help_message)

def main():
    os.system('clear')
    print_help()
    enter_to_continue()

    with open('resources/flashcards.csv') as cards:
        for card in cards:
            print('-------------------------------------')
            # list compression to get rid of leading spaces after the comma
            card = [s.strip() for s in card.split(',')]
            front = card[0]
            back = card[1]
            
            print(front)
            wait_for_enter()
            print(back)
            print('')

if __name__ == '__main__':
    main()  
