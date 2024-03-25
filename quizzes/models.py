from django.db import models
from users.models import User

class Session(models.Model):
    title = models.CharField(max_length=255, default='Untitled Session')
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Question(models.Model):
    question_types = [('multiple', 'Multiple Choices'), ('match', 'Match Answer'), ('simple', 'Simple Question'), ('true_false', 'True False'), ('fill', 'Fill Blank')]
    type = models.CharField(max_length=16, choices=question_types, default='simple')
    text = models.TextField(null=False, blank=False)
    question = models.TextField(null=False, blank=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return self.question