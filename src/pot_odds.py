import os, sys, random
from pprint import pprint
import readchar

def enter_to_continue():
    enter_message = "Press enter to continue."
    __ = input(enter_message)


def print_help():
    help_message = "Pot odds tell you what you stand to win relative to what you are risking.  Here is an example, pot is at 9bb and villain bets all-in at 9bb making the pot 18bb.  To stay in you must call 9bb.  The pot odds are 2:1 (reward:risk)."
    print(help_message)

def generate_whole_odds(calls = 0, scaleUp = True):
    # Odds = (pot + bet) : your call
    # Odds = (pot + bet*(number of calls + 1)) / your call
    # bet = pot / (odds - <number of calls + 1>)
    
    options = random.sample(range(1+calls+1,10), 4)
    correct = options[random.randint(0,3)]
    scale = (correct - (1+calls)) if scaleUp else 1
    pot = random.randint(1, 20) * scale
    bet = int(pot / (correct - (1 + calls)))

    return (options, correct, pot, bet)

def main():
    os.system('clear')
    print_help()
    enter_to_continue()

    input_key = 0

    num_correct = 0
    num_tries = 0

    while(1):
        print("-------------------------------------")
        (options, correct, pot, bet) = generate_whole_odds()

        message = "Pot: {}bb, Villain Bet: {}bb\nWhat are the odds: ".format(pot, bet)
        print(message)
        keys = ['a','s','d','f']
        for o,k in zip(options,keys):
            print("{K}-> {O}:1, ".format(K=k,O=o), end='')
        print("\nMake selection (q to quit): ", end='')

        input_key = readchar.readkey().lower()
        print("") # newline

        # '\x03' = Ctl+c
        # '\x04' = Ctl+d
        if (input_key == 'q' 
            or input_key == '\x03' 
            or input_key == '\x04'):
            break

        num_tries += 1

        if input_key in keys:
            i = keys.index(input_key)
            if options[i] == correct:
                print("Correct!")
                num_correct += 1
            else:
                print("Error: Correct answer was {}:1, you selected {}:1".format(correct, options[i]))
        else:
            print("Invalid input: {}".format(input_key))

        print("{} + {} = {}".format(pot,bet,pot+bet))
        print("{} / {} = {}".format(pot+bet,bet,(pot+bet)/bet))

        print("{} of {} correct, {:0.2f}%".format(num_correct, num_tries, num_correct/num_tries*100))

if __name__ == '__main__':
    main()
