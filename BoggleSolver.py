from math import sqrt
import numpy


class BoggleSolver:
    def __init__(self):
        # Initialize Letter Grid
        self.max_word_len = 6  # CONFIGURE
        self.N = 0
        self.letters = []
        self.used = []
        self.words = []
        self.wordlist = []
        bad_input = True
        while bad_input:
            input_str = input("Letters: ")
            self.N = int(sqrt(len(input_str)))
            if self.N*self.N != len(input_str):
                print("Typo, Not a square!")
                continue
            self.N += 2  # Adding rows/cols around
            self.letters = [['-' for _ in range(self.N)] for _ in range(self.N)]
            self.used = [[False for _ in range(self.N)] for _ in range(self.N)]
            counter = 0
            for r in range(self.N):
                for c in range(self.N):
                    if r == 0 or r == self.N-1 or c == 0 or c == self.N-1:
                        self.used[r][c] = True
                    else:
                        self.letters[r][c] = input_str[counter].lower()
                        counter += 1
            print(numpy.matrix(self.letters))
            user_happy = input("Look ok? (y/n)")
            if user_happy != "y":
                continue
            bad_input = False

    def parse_wordlist(self):
        wordlist_file = open("word-list.txt", "r")
        data = wordlist_file.read()
        self.wordlist = data.split("\n")
        wordlist_file.close()

    def begin_solving(self):
        # Begin Solving
        for r in range(self.N):
            for c in range(self.N):
                self.create_words(r, c, "", 0)

    def create_words(self, row, col, word_string, word_len):
        # Recursively try each letter permutation
        if self.used[row][col] or word_len > self.max_word_len:
            return
        self.used[row][col] = True
        word_string += self.letters[row][col]
        word_len += 1
        if self.is_word(word_string):
            self.words.append(word_string)
        self.create_words(row-1, col-1, word_string, word_len)
        self.create_words(row-1, col, word_string, word_len)
        self.create_words(row-1, col+1, word_string, word_len)
        self.create_words(row, col-1, word_string, word_len)
        self.create_words(row, col+1, word_string, word_len)
        self.create_words(row+1, col-1, word_string, word_len)
        self.create_words(row+1, col, word_string, word_len)
        self.create_words(row+1, col+1, word_string, word_len)
        self.used[row][col] = False

    def is_word(self, word_string):
        return word_string in self.wordlist

    def sort_words(self):
        self.words = sorted(self.words, key=len)

    def print_words(self):
        print(self.words)


def main():
    solver = BoggleSolver()
    solver.parse_wordlist()
    solver.begin_solving()
    solver.sort_words()
    solver.print_words()


if __name__ == '__main__':
    main()
