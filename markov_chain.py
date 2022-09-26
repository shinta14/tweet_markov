import re
import MeCab
from collections import deque


f = open('akutagawa.txt', 'r')

data = f.read()

def wakati(text):
    t = MeCab.Tagger("-Owakati")
    parsed_text = ""
    for one_line_text in one_sentence_generator(text):
        parsed_text += " "
        parsed_text += t.parse(one_line_text)
    wordlist = parsed_text.rstrip("\n").split(" ")
    return wordlist

def one_sentence_generator(long_text):
    sentences = re.findall(".*?。", long_text)
    for sentence in sentences:
        yield sentence

max_len = 2
queue = deque([], max_len)

def make_model(text, order=2):
    model = {}
    wordlist = wakati(text)
    queue = deque([], order)
    queue.append("[BOS]")
    for markov_value in wordlist:
        if len(queue) < order:
            queue.append(markov_value)
            continue

        if queue[-1] == "。":
            markov_key = tuple(queue)
            if markov_key not in model:
                model[markov_key] = []
            model.setdefault(markov_key, []).append("[BOS]")
            queue.append("[BOS]")
        markov_key = tuple(queue)
        model.setdefault(markov_key, []).append(markov_value)
        queue.append(markov_value)
    return model

import random

def make_sentence(model, sentence_num=1, seed="[BOS]", max_words = 1000):    
    sentence_count = 0

    key_candidates = [key for key in model if key[0] == seed]
    if not key_candidates:
        print("Not find Keyword")
        return
    markov_key = random.choice(key_candidates)
    queue = deque(list(markov_key), len(list(model.keys())[0]))

    sentence = "".join(markov_key)
    for _ in range(max_words):
        markov_key = tuple(queue)
        next_word = random.choice(model[markov_key])
        sentence += next_word
        queue.append(next_word)

        if next_word == "。":
            sentence_count += 1
            if sentence_count == sentence_num:
                break
    return sentence


text= data
order = 5
model = make_model(text)
sentence = make_sentence(model)
print(sentence)



f.close()
   