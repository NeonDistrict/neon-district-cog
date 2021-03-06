import sys
import os
import json
import math
import string
import jellyfish
import random

from jellyfish._jellyfish import damerau_levenshtein_distance

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def find_match(phrase, twitter = False):

    filename = 'lines.json' if twitter else 'lines.json'

    with open(os.path.join(__location__, filename), "r") as f:
        data = f.read()
        d = json.loads(data)

    # Remove punctuation and go to lowercase
    if isinstance(phrase, str):
        phrase = unicode(phrase, "utf-8")

    phrase = phrase.translate(remove_punctuation_map)
    phrase = phrase.lower()

    if not twitter:
        final_answer = "".join([c for c in phrase if c in string.letters or c in string.digits])
        if final_answer == "runprogram1nteroperabl3dat4sys7em" or final_answer == "runprograminteroperabledatasystem":
            return '<video width="320" height="240" autoplay src="https://s3.amazonaws.com/neon-district-easter-egg/b33bf85a8fff8ff65f172e07d128b810.mov"></video><audio autoplay><source src="https://s3.amazonaws.com/neon-district-easter-egg/f405f60b8acfdb9093a65e9516eee924.wav" type="audio/wav"></audio>', "sadness", "raw"

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

            res = damerau_levenshtein_distance(phrase, text)
            if res <= math.log(len(text), 3):
                # Take the next one
                if i < len(d_set) - 1:
                    row = d_set[i+1]
                    row['distance'] = res

                    # If we're using twitter, and there is twitter text, use it
                    if twitter and 'twitter' in row:
                        row['text'] = row['twitter']

                    # If the answers are a list, pick one
                    if isinstance(row['text'], list):
                        row['text'] = random.choice(row['text'])

                    if smallest_match is None or row['distance'] < smallest_match['distance']:
                        smallest_match = row

    if smallest_match is not None:
        # Don't send HTML over twitter
        text = smallest_match['text'].strip()
        if twitter and text.startswith('<img'):
            return None, None, None

        if 'activity' in smallest_match:
            return smallest_match['text'].strip(), smallest_match['condition'], smallest_match['activity']
        else:
            return smallest_match['text'].strip(), smallest_match['condition'], None

    return None, None, None


if __name__ == '__main__':
    if len(sys.argv) > 1:
        phrase = sys.argv[1]
        print find_match(phrase, twitter = False)
    else:
        print 'python cog.py "phrase here for testing"'
