from IPython import display
import preprocessing
import json

import numpy as np
import pandas as pd

import hazm
import requests
import time

import torch
from sentence_transformers import models, SentenceTransformer, util
from sklearn.cluster import KMeans

sentence_broken_file = open('../data/sentence_broken/sentences.json', 'w', encoding='utf8')
bert_sentence = open('../data/bert_gen/bert_sentence.json', 'w', encoding='utf8')


def rtl_print(outputs, font_size="15px", n_to_br=False):
    outputs = outputs if isinstance(outputs, list) else [outputs]
    if n_to_br:
        outputs = [output.replace('\n', '<br/>') for output in outputs]

    outputs = [f'<p style="text-align: right; direction: rtl; margin-right: 10px; font-size: {font_size};">{output}</p>'
               for output in outputs]
    display.display(display.HTML(' '.join(outputs)))


def load_st_model(model_name_or_path):
    word_embedding_model = models.Transformer(model_name_or_path)
    pooling_model = models.Pooling(
        word_embedding_model.get_word_embedding_dimension(),
        pooling_mode_mean_tokens=True,
        pooling_mode_cls_token=False,
        pooling_mode_max_tokens=False)

    model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
    return model


# Corpus with example sentences
corpus = sentence_broken_file

num_clusters = 3


json_filename = '../data/sentence_broken/sentences.json'

embedder = load_st_model(json_filename)
corpus_embeddings = embedder.encode(corpus, show_progress_bar=True)


# Perform kmean clustering
clustering_model = KMeans(n_clusters=num_clusters)
clustering_model.fit(corpus_embeddings)
cluster_assignment = clustering_model.labels_

clustered_sentences = [[] for i in range(num_clusters)]
for sentence_id, cluster_id in enumerate(cluster_assignment):
    clustered_sentences[cluster_id].append(corpus[sentence_id])

for i, sentences in enumerate(clustered_sentences):
    rtl_print(f'Cluster: {i + 1}', '20px')
    rtl_print(sentences)
    rtl_print('- - ' * 50)
    bert_sentence.append({
        'id': i,
        'text': sentences
    })

