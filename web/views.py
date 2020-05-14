from django.http import JsonResponse
import numpy as np
from keras.models import load_model
from .models import Model, Sentence


def classify(request):
    selected_model = Model.objects.all()[0]
    model_path = selected_model.path
    model = load_model(model_path)

    text = request.POST.get('text')
    X_train_indices = selected_model.sentences_to_indices(str(text))
    pred = model.predict(X_train_indices)
    emoji_idx = np.argmax(pred[0])
    prob = pred[0][emoji_idx]
    sentence = Sentence(text=text, prob=prob)

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
    sentence.emoji = emoji
    sentence.save()
    return JsonResponse(data={'emoji': emoji,
                              'prob': prob})