from __future__ import unicode_literals
import json
from hazm import *

normalizer = Normalizer()
lemmatizer = Lemmatizer()

stop_words_file = open('../data/raw/stopwords-fa.txt')
stop_words = [i for i in stop_words_file.read().splitlines()]

raw_dataset_file = open('../data/raw/raw_dataset.json', 'r', encoding='utf8')
cleaned_dataset_file = open('../data/cleaned/cleaned_dataset.json', 'w', encoding='utf8')
sentence_broken_file = open('../data/sentence_broken/sentences.json', 'w', encoding='utf8')
word_broken_file = open('../data/word_broken/words.txt', 'w', encoding='utf8')

raw_dataset = json.load(raw_dataset_file)
cleaned_text_data = []
sentences_data = []
sentence_counter = 1
main_counter = 1

for row in raw_dataset:
    cleaned_text = normalizer.normalize(row.get('text'))
    cleaned_text_data.append({
        'id': row.get('id'),
        'text': cleaned_text,
        'subject': row.get('title')
    })

    for sentence in sent_tokenize(cleaned_text):
        sentences_data.append({
            'id': sentence_counter,
            'text': sentence,
            'subject': row.get('title')
        })
        sentence_counter += 1

    for word in word_tokenize(cleaned_text):
        new_word = lemmatizer.lemmatize(word)
        if new_word not in stop_words:
            word_broken_file.write(new_word + '\n')

    print(str(main_counter) + " from " + str(len(raw_dataset)) + " (", end='')
    print("%4.2f"%((main_counter / len(raw_dataset)) * 100), end='')
    print("%)")
    main_counter += 1

cleaned_dataset_file.write(json.dumps(cleaned_text_data, ensure_ascii=False))
sentence_broken_file.write(json.dumps(sentences_data, ensure_ascii=False))

cleaned_dataset_file.close()
word_broken_file.close()
sentence_broken_file.close()
