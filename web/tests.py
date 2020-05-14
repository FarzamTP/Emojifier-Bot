import numpy as np

X_indices = np.zeros((1, 32))
sentence_words = [word.lower().replace('\t', '') for word in "Hello I am A boy".split(' ') if
                      word.replace('\t', '') != '']

print(X_indices)
print(sentence_words)