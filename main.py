import random
import sys
import time
""" Monty Hall: Empirical proof to switch doors!

The Monty Hall problem is often used to illustrate the less intuitive concepts in Probability theory.
However, it is very hard to explain, even to Math-inclined people. I remember that I never understood
the correct solution until I attempted a simulation back in 2010.

After discussing the problem with a colleague, I decided to write a simulation again. Below is the product
of my labour.

Pull Requests and Github Issues welcome! Any other feedback as well ;)

Written by Arie Roos (arie@itecho.co.za)
"""


class Counters:
    switch = 0
    stay = 0

    def __init__(self):
        self.switch = 0
        self.stay = 0

    def print_stats(self):
        total = self.switch + self.stay
        switch_percentage = (self.switch / total) * 100
        stay_percentage = (self.stay / total) * 100

        print("Total games: ", total)
        print("It was the chosen door {0} times. ({1}%)".format(
            self.stay, stay_percentage))
        print("It was the other door {0} times. ({1}%)".format(
            self.switch, switch_percentage))


class Doors:
    # Doors have the following states:
    #   0: closed (normal)
    #   1: closed (prize)
    #   2: open (garbage)
    #   3: open (prize)
    #   4: chosen (normal)
    #   5: chosen (prize)
    #   6: chosen (lost)
    #   7: chosen (won)
    doors = [0, 0, 0]

    def __init__(self):
        self.doors = [0, 0, 0]

    def set_winner(self):
        winner = random.randint(0, 2)
        self.doors[winner] = 1
        return winner + 1

    def choose(self, choice):
        choice -= 1
        self.doors[choice] += 4

    def reveal(self):
        choices = []
        for i, door in enumerate(self.doors):
            if door == 0:
                choices.append(i)

        choice = random.choice(choices)
        self.doors[choice] += 2
        return choice + 1

    def switch(self):
        for i, door in enumerate(self.doors):
            if door in [0, 1]:
                self.doors[i] += 4
            elif door in [4, 5]:
                self.doors[i] -= 4

    def resolve(self):
        won = False
        for i, door in enumerate(self.doors):
            if door != 2:
                self.doors[i] += 2
                if self.doors[i] == 7:
                    won = True
        return won

    def print(self):
        for door in self.doors:
            {0: lambda: print("[\u25A0]", end=''),
             1: lambda: print("[\u25A0]", end=''),
             2: lambda: print("[g]", end=''),
             3: lambda: print("[p]", end=''),
             4: lambda: print("[*]", end=''),
             5: lambda: print("[*]", end=''),
             6: lambda: print("[G]", end=''),
             7: lambda: print("[P]", end='')}[door]()
        print()


def print_sep():
    print("------------------------------------------")


def play():
    doors = Doors()
    doors.set_winner()
    print("Two doors have (g)arbage behind them, the other one a (p)rize!")

    option = 0
    while option not in [1, 2, 3]:
        doors.print()
        optionIn = input("Pick a door! (Enter 1,2 or 3): ")
        option = int(optionIn) if optionIn.isdigit() else 0

    print("You picked door number {}.".format(option))
    doors.choose(option)
    doors.print()

    print("Now, let me open another door", end='')
    for _ in range(3):
        time.sleep(0.5)
        print(".", end='')
        sys.stdout.flush()
    print()
    doors.reveal()
    doors.print()

    switch = 'q'
    while switch not in ['y', 'n']:
        switch = input("Do you want to switch(y/n)? ").lower()
    if switch == 'y':
        doors.switch()
    doors.print()

    print("Let's see if you won", end='')
    for _ in range(3):
        time.sleep(0.75)
        print(".", end='')
        sys.stdout.flush()
    print()

    won = doors.resolve()
    doors.print()
    if won and switch == 'y':
        counters.switch += 1
        print("YOU WON! Well done for understanding probabilities ;)")
    if won and switch == 'n':
        counters.stay += 1
        print("YOU WON! You may be stubborn, but at least you are lucky!")
    if not won and switch == 'y':
        counters.stay += 1
        print("You lost. Bad luck :(")
    if not won and switch == 'n':
        counters.switch += 1
        print("You lost. You should've switched.")

    print_sep()


def simulate():
    count = 0
    while count < 2 or count > 100000:
        countStr = input(
            "How many times should I simulate the game? (Enter a number between 2 and 100 000): ")
        countStr = countStr.replace(" ", "")
        try:
            count = int(countStr)
        except ValueError:
            count = 0

    print_all = (count < 1001)
    skip_counts = (count > 10001)

    if not print_all:
        print("Not printing details. If you want to see details, pick a number below 1000.")

    sim_stats = Counters()
    for i in range(1, count + 1):
        if not skip_counts or i % 100 == 0 or i == count:
            print("Simulation {0}:".format(i))

        doors = Doors()
        winner = doors.set_winner()
        choice = random.randint(1, 3)
        doors.choose(choice)
        if print_all:
            print("\tPlayer chooses door {}.".format(choice))
            print("\tPresenter reveals door {}.".format(doors.reveal()))
            print("\tThe winning door is {}.".format(winner))
        
        if winner == choice:
            if print_all:
                print("Player should stay.")
            counters.stay += 1
            sim_stats.stay += 1
        else:
            if print_all:
                print("Player should switch.")
            counters.switch += 1
            sim_stats.switch += 1

    print("Simulation Done:")
    sim_stats.print_stats()
    print_sep()


print("Welcome to Monty Hall!")
counters = Counters()
first_play = True
quit_game = False
while not quit_game:
    option = 'x'
    while option not in ['p', 's', 'm', 'q']:
        print("What do you want to do?")
        if first_play:
            print("(p)lay")
        else:
            print("(p)lay again")
        print("Simulate (m)any games")
        print("Print (s)tats")
        print("(q)uit")
        option = input()[0].lower()

    print_sep()
    if option == 'p':
        first_play = False
        play()
    if option == 's':
        print("Global Stats:")
        counters.print_stats()
        print_sep()
    if option == 'm':
        simulate()
    if option == 'q':
        quit_game = True
