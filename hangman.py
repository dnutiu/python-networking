#! usr/bin/python3
"A simple Hangman program"
import string
import random

class Hangman:
    """ A simple Hangman class for playing the hangman game. """
    words = ["test", "test2"] # TODO Make a new way of generating words, perhaps a file?
    def __init__(self):
        random.seed(None) # Use current system time when generating random nums

        self.word = random.choice(self.words)
        self.obscured_word = ["*" for i in self.word]
        self.letters = [] # Already guessed letters
        self.lives = 9
        self.guesses_left = len(self.word)
        self.game_status = 0 # 0 - on going, 1 - won, 2 - lost

    def _is_in_word(self, guess):
        """Returns the index position of the guess from the word"""
        return self.word.find(guess)

    def _modify_word(self, letter):
        self.word = self.word.replace(letter, "_")

    def _modify_obscured_word(self, letter, starting_pos=0):
        """ Modifies the obscured world, by revealing guessed letters """
        index = self.word.find(letter, starting_pos)
        if index >= 0:
            self.obscured_word[index] = letter
            self.guesses_left -= 1
            self._modify_obscured_word(letter, index + 1)

    def _perfom_guess(self, letter):
        """ Performs the guess by validating the guessed letter. """
        if letter in string.ascii_letters:
            self.letters.append(letter)
            if self._is_in_word(letter) >= 0:
                print("You guessed right!")
                self._modify_obscured_word(letter)
                self._modify_word(letter)
                self.update_game_status()
            else:
                print("{} is not in the word. :(".format(letter))
                self.lives -= 1
                self.update_game_status()
        else:
            print("You need to chose a letter. {} is not a letter!"
                  .format(letter))
            print("You lost a life.")
            self.lives -= 1
            self.update_game_status()

    def victory(self):
        """ Prints victory message and sets game status to win """
        print("Congratulations! You won the game!")
        self.game_status = 1

    def defeat(self):
        """ Prints defeat message and sets game status to lost """
        print("Congratulations! You lost the game!")
        self.game_status = 2

    def update_game_status(self):
        """ Updates the game status. """
        if self.guesses_left == 0:
            self.victory()
        elif self.lives == 0:
            self.defeat()

    def announce(self):
        """ Announces the word and lives left """
        print("{} - You have {} lives left."
              .format("".join(map(str, self.obscured_word)), self.lives))

    def make_guess(self, letter):
        """ Makes the guess """
        letter = letter.lower()
        if letter in self.letters:
            print("You already said {}".format(letter))
        else:
            self._perfom_guess(letter)




hm = Hangman()
hm.announce()

hm.make_guess("t")
hm.make_guess("e")
hm.make_guess("s")
hm.announce()
