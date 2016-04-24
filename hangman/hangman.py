#! usr/bin/python3
"A simple Hangman program"
import string
import random
import csv

# TODO Add score perhaps?

class Hangman:
    """ A simple Hangman class for playing the hangman game. """
    words = []

    def __init__(self, broadcast_function=print):
        self._letter = "" # guessed letter, used internally
        self.broadcast = broadcast_function
        try:
            self._load_words()
            self.word = random.choice(self.words)
        except IndexError:
            print("Error: Cannot make choices!\n")
            self.word = "Error"
        except FileNotFoundError:
            print("Error: File words.csv not found!\n")
            self.word = "Error"

        self.original_world = self.word
        self.obscured_word = ["*" for i in self.word]
        self.guesses_left = len(self.word.replace(" ", "")) # remove spaces
        self.letters = [] # Already guessed letters
        self.lives = 9
        self.game_status = 0 # 0 - on going, 1 - won, 2 - lost

    def _load_words(self):
        try:
            with open("words.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    self.words += row
        except FileNotFoundError:
            raise FileNotFoundError

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
        message = "{} is not in the word. :(\n".format(self._letter)
        self.broadcast(message)
        self.lives -= 1
        self.update_game_status()

    def _good_guess(self):
        message = "You guessed right!\n"
        self.broadcast(message)
        self._modify_obscured_word()
        self._modify_word()
        self.update_game_status()

    def _invalid_guess(self):
        message = """You need to chose a letter. {} is not a letter!
You lost a life.\n""".format(self._letter)
        self.broadcast(message)
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
        message = "Starting new Hangman game!\n"
        print("Staring new game!")
        self.broadcast(message)
        self.__init__(self.broadcast)

    def victory(self):
        """ Prints victory message and sets game status to win """
        message = """Congratulations! You won the game!
The word was: {}\n""".format(self.original_world)
        print("Users achieved victory!")
        self.broadcast(message)

    def defeat(self):
        """ Prints defeat message and sets game status to lost """
        message = """Congratulations! You lost the game!
The word was: {}\n""".format(self.original_world)
        print("Users lost!")
        self.broadcast(message)

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
            message = "{} - You have {} lives left.\n".format(self._obscured_word_str(), self.lives)
            print(message)
            self.broadcast(message)

    def make_guess(self, letter):
        """ Makes the guess """
        self._letter = letter.lower()
        if self._letter in self.letters:
            message = "You already said {}\n".format(self._letter)
            self.broadcast(message)
        else:
            self._perfom_guess()
