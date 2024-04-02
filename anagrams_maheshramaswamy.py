# Given a words.txt file containing a newline-delimited list of dictionary
# words, please implement the Anagrams class so that the get_anagrams() method
# returns all anagrams from words.txt for a given word.
#
# Bonus requirements:
#   - Optimise the code for fast retrieval
#   - Write more tests
#   - Thread safe implementation

import unittest
from itertools import permutations

# Implementing and adding thread safety into the code.
from threading import Thread
from threading import Lock


class Anagrams:

    def __init__(self):
        self.thread_lock = Lock()
        self.words = []
        # Changed the reading of file to avoid newline charater being read.
        with open("DictionaryWords.txt") as file:
            self.words = file.read().splitlines()

        # Search optimization by inserting all the words into dictionary
        self.words_dict = {}
        for index, word in enumerate(self.words):
            self.words_dict[word.lower()] = index

    def get_anagrams(self, word):
        anagram_words = []

        # Acquire the thread lock for performing the permutation string calculation and de-duplication process.
        self.thread_lock.acquire()

        # Get all the permutations of the given word for the length of the word.
        permuation_words = permutations(word.lower(), len(word))
        for str_list in permuation_words:
            # The permutation function returns list of letters. Hence, need to join all the letters
            # and convert it into a single word/string.
            word = "".join(str_list)
            if word in self.words_dict:
                anagram_words.append(word)

        # Removing duplicates from the anagram words list. For example case of 'dreads' word.
        anagram_words = list(dict.fromkeys(anagram_words))
        self.thread_lock.release()

        return anagram_words


class TestAnagrams(unittest.TestCase):

    def test_anagrams(self):
        anagrams = Anagrams()
        # Changed the sequence of possible returnable words from the assertion results.
        self.assertEqual(anagrams.get_anagrams('plates'), ['plates', 'palest', 'pastel', 'petals', 'staple'])
        self.assertEqual(anagrams.get_anagrams('eat'), ['eat', 'ate', 'tea'])

        # Added few more test samples.
        # Positive case.
        self.assertEqual(anagrams.get_anagrams('plum'), ['plum', 'lump'])

        # Empty test
        self.assertEqual(anagrams.get_anagrams('coolant'), [])

        # Alphanumeric test.
        self.assertEqual(anagrams.get_anagrams('2Plant'), [])

        # Duplicates test with capital letters.
        self.assertEqual(anagrams.get_anagrams('Dreads'), ['dreads', 'adders', 'sadder'])
        self.assertEqual(anagrams.get_anagrams('drawer'), ['drawer', 'redraw', 'reward', 'warder', 'warred'])

        # Multiple Letters appearing multiple times test.
        self.assertEqual(anagrams.get_anagrams('vessel'), ['vessel', 'selves'])


if __name__ == '__main__':
    unittest.main()