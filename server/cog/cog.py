import sys
import os
import json
import math
import string
import jellyfish

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def find_match(phrase):
    with open(os.path.join(__location__, 'lines.json'), "r") as f:
        data = f.read()
        d = json.loads(data)

    # Remove punctuation and go to lowercase
    if isinstance(phrase, str):
        phrase = unicode(phrase, "utf-8")

    phrase = phrase.translate(remove_punctuation_map)
    phrase = phrase.lower()

    # Check each phrase for a match
    lines = d['lines']
    smallest_match = None
    for d_set in lines:
        for i in range(0, len(d_set), 2):
            if i >= len(d_set) - 1:
                continue

            row = d_set[i]

            text = row['text']
            text = text.translate(remove_punctuation_map)
            text = text.lower()

            res = jellyfish.damerau_levenshtein_distance(phrase, text)
            if res <= math.log(len(text), 1.82):
                # Take the next one
                if i < len(d_set) - 1:
                    row = d_set[i+1]
                    row['distance'] = res
                    if smallest_match is None or row['distance'] < smallest_match['distance']:
                        smallest_match = row

    if smallest_match is not None:
        if 'activity' in smallest_match:
            return smallest_match['text'].strip(), smallest_match['condition'], smallest_match['activity']
        else:
            return smallest_match['text'].strip(), smallest_match['condition'], None

    return None, None, None


if __name__ == '__main__':
    if len(sys.argv) > 1:
        phrase = sys.argv[1]
        print find_match(phrase)
    else:
        print 'python cog.py "phrase here for testing"'
