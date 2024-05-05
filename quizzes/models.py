from django.db import models
from users.models import User

class Session(models.Model):
    title = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f'Session {self.pk or ""}'
        super().save(*args, **kwargs)

class Question(models.Model):
    lang_types = [('arabic','arabic'),('english','english')]
    lang = models.CharField(max_length=16, choices=lang_types, default='arabic')
    text = models.TextField(null=False, blank=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    question = models.TextField(null=False, blank=False)
    answer = models.TextField(default='no answer')
    

    def __str__(self):
        return self.question