#!/usr/bin/python3

"""
Clean text and break into ngrams, then get the ngrams that occur most frequently
"""

import argparse
import re
import sys
from collections import Counter

# inspired by: https://albertauyeung.github.io/2018/06/03/generating-ngrams.html
def get_ngrams(text: str, n: int) -> list:
    """Parse the given text and return ngrams of the specified length."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    tokens = [ token for token in text.split(' ') if len(token) ]

    ngrams = zip(*[ tokens[i:] for i in range(n) ])
    return [ ' '.join(ngram) for ngram in ngrams ]

def is_valid(stopwords: list, phrase: str) -> bool:
    """Return True if the phrase contains no stopwords."""
    for word in stopwords:
        if re.match(rf'(^|.+)\b{word}\b($|.+)', phrase):
            return False
    return True

def analyze_text(text: str, numbers: str) -> Counter:
    """Clean text and count ngrams."""
    with open('stopwords.txt', encoding='utf-8') as fp:
        stopwords = [ word.strip() for word in fp.readlines() if len(word.strip()) ]

    ng = []
    for n in expand_numbers_list(numbers):
        ng.extend(get_ngrams(text, n))

    # make a list of phrases that don't contain any stopwords
    ngrams = [ phrase for phrase in ng if is_valid(stopwords, phrase) ]
    return Counter(ngrams)

def print_results(c: Counter, m=None) -> None:
    """Print the most common items in the Counter."""
    if not m:
        m = int(c.total() * 0.003)

    for item in c.most_common(m):
        phrase, count = item
        if count != 1:
            print(f'[*] occurrences: {count:<3} phrase: {phrase}')

def arg_parse():
    """Handle command line arguments."""
    parser = argparse.ArgumentParser(
            prog='ngrams analyzer',
            description='determine ngrams from text')
    parser.add_argument('-f', '--file', help='input file. defaults to stdin')
    parser.add_argument('-w', '--words', required=True,
            help='the number of words to look for. can be given as comma-seperated or as a range')
    parser.add_argument('-t', '--top', type=int,
            help='the top number of occurrences to print. defaults to the top 0.003 percent')

    return parser.parse_args()

def expand_numbers_list(items: str):
    """Expand a string of comma-seperated numbers and ranges into a list.
    
    Examples:
    items = '1,2,3' returns [1, 2, 3]
    items = '5-7' returns [5, 6, 7]
    items = '1,3-5' returns [1, 3, 4, 5]
    """
    for n in items.split(','):
        # if a range is specified
        num_range = n.split('-')
        if len(num_range) == 2:
            yield from range(int(num_range[0]), int(num_range[1])+1)
        # if it's just a number, not a range
        else:
            yield int(n)

def main():
    """Main function."""
    args = arg_parse()
    text = ''
    if args.file:
        with open(args.file, encoding='utf-8') as fp:
            text = fp.read()
    # if a file name isn't given, read from stdin
    else:
        text = ''.join([ line.strip() for line in sys.stdin ])

    counter = analyze_text(text, args.words)
    print_results(counter, args.top)


if __name__ == '__main__':
    main()
