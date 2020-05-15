from django.http import JsonResponse
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from .models import Sentence
import pandas as pd

np.warnings.filterwarnings('ignore')

from keras.models import load_model


def read_glove_vecs(file_path):
    print("Loading Glove Model..")
    f = open(file_path, 'r', errors='ignore', encoding='utf8')
    gloveModel = {}
    words = set()
    for line in f:
        try:
            splitLines = line.split()
            word = splitLines[0]
            words.add(word)
            wordEmbedding = np.array([float(value) for value in splitLines[1:]])
            gloveModel[word] = wordEmbedding
        except:
            pass

    i = 1
    words_to_index = {}
    index_to_words = {}
    for w in sorted(words):
        words_to_index[w] = i
        index_to_words[i] = w
        i = i + 1
    print(len(gloveModel), "words loaded!")
    return words_to_index, index_to_words, gloveModel


def sentences_to_indices(X, word_to_index, max_len):
    X_indices = np.zeros((1, max_len))
    sentence_words = [word.lower().replace('\t', '') for word in X[0].split(' ') if
                      word.replace('\t', '') != '']
    j = 0
    for w in sentence_words:
        X_indices[0, j] = word_to_index[w]
        j += 1
    return X_indices


word_to_index, index_to_words, word_to_vec_map = read_glove_vecs('/var/www/EmojifierBot/GloVe/glove.6B.50d.txt')


@csrf_exempt
def classify(request):
    model_path = '/var/www/EmojifierBot/model/model.h5'

    model = load_model(model_path)
    text = request.POST.get('text')
    X_train_indices = sentences_to_indices(np.asarray([str(text)]), word_to_index, 10)
    pred = model.predict(X_train_indices)
    emoji_idx = np.argmax(pred[0])
    prob = pred[0][emoji_idx]

    if emoji_idx == 0:
        emoji = ':heart:'
    elif emoji_idx == 1:
        emoji = ":baseball:"
    elif emoji_idx == 2:
        emoji = ":smile:"
    elif emoji_idx == 3:
        emoji = ":disappointed:"
    else:
        emoji = ":fork_and_knife:"

    sentence = Sentence(text=text, prob=prob, predicted_emoji=emoji)
    sentence.save()

    return JsonResponse(data={'emoji': str(emoji),
                              'prob': str(prob),
                              'sentence_id': sentence.id})


@csrf_exempt
def submit(request):
    action = request.POST.get('action')
    sentence_id = request.POST.get('sentence_id')
    emoji_unicode = request.POST.get('emoji_unicode')

    sentence = Sentence.objects.all().filter(pk=int(sentence_id))[0]

    sentence.assigned_label = emoji_unicode

    if action == 'like':
        sentence.feedback = 'like'
    elif action == 'label':
        sentence.feedback = 'dislike'

    sentence.save()
    return JsonResponse(data={'status': 200})


@csrf_exempt
def export_to_csv(request):
    data = pd.DataFrame(columns=['Text', 'Predicted', 'Feedback', 'Labeled', 'Probability'])

    sentences = Sentence.objects.all()

    for idx, sentence in enumerate(sentences):
        data.loc[idx] = [sentence.text, sentence.predicted_emoji, sentence.feedback, sentence.assigned_label, sentence.prob]

    # data.to_csv('./data.csv')
    return JsonResponse(data={'data': str(data)})
