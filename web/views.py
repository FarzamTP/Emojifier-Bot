from django.http import JsonResponse
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from keras.models import load_model
from .models import Sentence


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
    m = X.shape[0]
    X_indices = np.zeros((m, max_len))
    for i in range(m):
        sentence_words = [word.lower().replace('\t', '') for word in X[i].split(' ') if
                          word.replace('\t', '') != '']
        j = 0
        for w in sentence_words:
            X_indices[i, j] = word_to_index[w]
            j += 1
    return X_indices


word_to_index, index_to_words, word_to_vec_map = read_glove_vecs('/var/www/EmojifierBot/GloVe/glove.6B.50d.txt')


@csrf_exempt
def classify(request):
    model_path = '/var/www/EmojifierBot/model/model.h5'

    model = load_model(model_path)
    text = request.POST.get('text')
    X_train_indices = sentences_to_indices(np.asarray([str(text)]), word_to_index, 50)
    # pred = model.predict(X_train_indices)
    # emoji_idx = np.argmax(pred[0])
    # print("Emoji idx:", emoji_idx)
    # prob = pred[0][emoji_idx]
    # print("Prob:", prob)
    #
    # sentence = Sentence(text=text, prob=prob)
    #
    # if emoji_idx == 0:
    #     emoji = ':heart:'
    # elif emoji_idx == 1:
    #     emoji = ":baseball:"
    # elif emoji_idx == 2:
    #     emoji = ":smile:"
    # elif emoji_idx == 3:
    #     emoji = ":disappointed:"
    # else:
    #     emoji = ":fork_and_knife:"
    # sentence.emoji = emoji
    # sentence.save()
    # print("Emoji:", emoji)
    # return JsonResponse(data={'emoji': emoji,
    #                           'prob': prob})
    return JsonResponse(data={'status': X_train_indices,
                              'model': str(model)})
