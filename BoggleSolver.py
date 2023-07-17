from math import sqrt
import numpy


class BoggleSolver:
    def __init__(self):
        # Initialize Letter Grid
        # agianttesderealcecetsvjaioepsfeounrlagctslgrciulsnwnldznoptiaobm
        self.desired_word_len = 6  # CONFIGURE
        self.N = 0
        self.letters = []
        self.used = []
        self.words = []
        self.wordlist_full = []
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
            print('\n')
            bad_input = False

    def parse_wordlist(self):
        wordlist_file = open("word-list.txt", "r")
        data = wordlist_file.read()
        self.wordlist_full = data.split("\n")
        self.wordlist_full = {idx for idx in self.wordlist_full if len(idx) == self.desired_word_len}
        wordlist_file.close()

    def begin_solving(self):
        # Begin Solving
        for r in range(self.N):
            for c in range(self.N):
                self.filter_wordlist_by_first_letter(self.letters[r][c])
                self.create_words(r, c, "", 0)

    def filter_wordlist_by_first_letter(self, first_letter):
        # Note the curly brackets! Searching sets is O(1). Sets are implemented using hash tables.
        self.wordlist = {idx for idx in self.wordlist_full if idx[0] == first_letter}

    def create_words(self, row, col, word_string, word_len):
        # Recursively try each letter permutation
        if self.used[row][col] or word_len == self.desired_word_len:
            return
        self.used[row][col] = True
        word_string += self.letters[row][col]
        word_len += 1
        if word_len == self.desired_word_len and self.is_word(word_string):
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
        self.words = set(self.words)
        for word in self.words:
            print(word)


def main():
    solver = BoggleSolver()
    solver.parse_wordlist()
    solver.begin_solving()
    solver.sort_words()
    solver.print_words()


if __name__ == '__main__':
    main()
