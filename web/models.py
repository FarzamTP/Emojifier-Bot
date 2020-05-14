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
