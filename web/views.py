from django.http import HttpResponse
from django.shortcuts import render
from keras.models import load_model

model = load_model('./models/model.h5')

def classify(request):
    model.