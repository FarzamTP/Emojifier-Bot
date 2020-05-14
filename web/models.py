from django.db import models
import numpy as np


class Sentence(models.Model):
    text = models.CharField(max_length=1024, default=None, blank=True)
    prob = models.FloatField(blank=True, default=0.0)

    none = 'none'
    heart = ':heart:'
    baseball = ':baseball:'
    smile = ':smile:'
    disappointed = ':disappointed:'
    fork_and_knife = ':fork_and_knife:'

    emoji_choices = (
        (none, 'none'),
        (heart, ':heart:'),
        (baseball, ':baseball:'),
        (smile, ':smile:'),
        (disappointed, ':disappointed:'),
        (fork_and_knife, ':fork_and_knife:')
    )

    emoji = models.CharField(blank=True, choices=emoji_choices, default=none, max_length=32)

    none = "none"
    like = "like"
    dislike = "dislike"

    feedback_choices = (
        (none, "none"),
        (like, "like"),
        (dislike, 'dislike'),
    )

    feedback = models.CharField(blank=True, choices=feedback_choices, default=none, max_length=32)


class Model(models.Model):
    path = models.CharField(default='./model/model.h5')

    def sentences_to_indices(self, X, word_to_index, max_len):
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

