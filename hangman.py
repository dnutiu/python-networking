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
        self.letter = "" # guessed letters # TODO Remove letter param from func
        self.lives = 9
        self.guesses_left = len(self.word)
        self.game_status = 0 # 0 - on going, 1 - won, 2 - lost

    def _obscured_word_str(self):
        """ Transforms obscured_word arrat into a string. """
        return "".join(i for i in self.obscured_word)

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

    def _bad_guess(self, letter):
        print("{} is not in the word. :(".format(letter))
        self.lives -= 1
        self.update_game_status()

    def _good_guess(self, letter):
        print("You guessed right!")
        self._modify_obscured_word(letter)
        self._modify_word(letter)
        self.update_game_status()

    def _invalid_guess(self, letter):
        print("You need to chose a letter. {} is not a letter!"
              .format(letter))
        print("You lost a life.")
        self.lives -= 1
        self.update_game_status()

    def _perfom_guess(self, letter):
        """ Performs the guess by validating the guessed letter. """
        if letter in string.ascii_letters:
            self.letters.append(letter)
            if self._is_in_word(letter) >= 0:
                self._good_guess(letter)
            else:
                self._bad_guess(letter)
        else:
            self._invalid_guess(letter)

    def victory(self):
        """ Prints victory message and sets game status to win """
        print("Congratulations! You won the game!")
        print("The word was: {}".format(self._obscured_word_str()))

    def defeat(self):
        """ Prints defeat message and sets game status to lost """
        print("Congratulations! You lost the game!")
        print("The word was: {}".format(self._obscured_word_str()))

    def game_over(self):
        if self.game_status == 1:
            self.victory()
        elif self.game_status == 2:
            self.defeat()

    def get_game_status(self):
        """ Returns the game status. 1 - won, 2 - lost, 0 on going"""
        return self.game_status

    def update_game_status(self):
        """ Updates the game status. """
        if self.guesses_left == 0:
            self.game_status = 1
        elif self.lives == 0:
            self.game_status = 2

    def announce(self):
        """ Announces the word and lives left or if the game has ended. """
        if self.game_status == 1:
            self.victory()
        elif self.game_status == 2:
            self.defeat()
        else:
            print("{} - You have {} lives left."
                  .format(self._obscured_word_str(), self.lives))

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
hm.announce()
hm.make_guess("e")
hm.announce()
hm.make_guess("s")
hm.announce()
