from django.db import models
from django.contrib.auth.models import AbstractUser

class Word(models.Model):
    expression = models.CharField(max_length=32)
    description = models.CharField(max_length=1024)
    gre_synonym = models.ManyToManyField('self', blank=True)
    PARTS_OF_SPEECH = (
        ('V', 'Verb'),
        ('N', 'Noun'),
        ('P', 'Pronoun'),
        ('A', 'Adjective'),
        ('AV', 'Adverb'),
        ('PP', 'Preposition'),
        ('C', 'Conjunction'),
        ('AC', 'Article'),
        ('E', 'Expression')
    )
    part_of_speech = models.CharField(max_length=2, choices=PARTS_OF_SPEECH)

    #def __str__(self):
    #    return f"{self.expression}"

class User(AbstractUser):
    pass