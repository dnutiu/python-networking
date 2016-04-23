#! usr/bin/python3
"A simple Hangman program"
import string
import random

class Hangman:
    """ A simple Hangman class for playing the hangman game. """
    words = ["test", "test2"] # TODO Make a new way of generating words, perhaps a file?
    def __init__(self):
        self._letter = "" # guessed letter, used internally
        random.seed(None) # Use current system time when generating random nums

        self.word = random.choice(self.words)
        self.obscured_word = ["*" for i in self.word]
        self.letters = [] # Already guessed letters
        self.lives = 9
        self.guesses_left = len(self.word)
        self.game_status = 0 # 0 - on going, 1 - won, 2 - lost

    def _obscured_word_str(self):
        """ Transforms obscured_word arrat into a string. """
        return "".join(i for i in self.obscured_word)

    def _letter_is_in_word(self):
        """Returns the index position of the guess from the word"""
        return self.word.find(self._letter)

    def _modify_word(self):
        self.word = self.word.replace(self._letter, "_")

    def _modify_obscured_word(self, starting_pos=0):
        """ Modifies the obscured world, by revealing guessed letters """
        index = self.word.find(self._letter, starting_pos)
        if index >= 0:
            self.obscured_word[index] = self._letter
            self.guesses_left -= 1
            self._modify_obscured_word(index + 1)

    def _bad_guess(self):
        print("{} is not in the word. :(".format(self._letter))
        self.lives -= 1
        self.update_game_status()

    def _good_guess(self):
        print("You guessed right!")
        self._modify_obscured_word()
        self._modify_word()
        self.update_game_status()

    def _invalid_guess(self):
        print("You need to chose a letter. {} is not a letter!"
              .format(self._letter))
        print("You lost a life.")
        self.lives -= 1
        self.update_game_status()

    def _perfom_guess(self):
        """ Performs the guess by validating the guessed letter. """
        if self._letter in string.ascii_letters:
            self.letters.append(self._letter)
            if self._letter_is_in_word() >= 0:
                self._good_guess()
            else:
                self._bad_guess()
        else:
            self._invalid_guess()

    def new_game(self):
        print("Starting new Hangman game!")
        self.__init__()

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
        self._letter = letter.lower()
        if self._letter in self.letters:
            print("You already said {}".format(self._letter))
        else:
            self._perfom_guess()




hm = Hangman()
hm.announce()

hm.make_guess("t")
hm.announce()
hm.make_guess("e")
hm.announce()
hm.make_guess("s")
hm.announce()
hm.new_game()
hm.announce()
