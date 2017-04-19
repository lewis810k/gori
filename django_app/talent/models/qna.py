from django.conf import settings
from django.db import models

from member.models import Tutor
from talent.models import Talent

__all__ = (
    'Question',
    'Reply',
)


class Question(models.Model):
    talent = models.ForeignKey(Talent)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Talent : {} User : {}'.format(self.talent.title, self.user.name)

    def content_summary(self):
        if len(self.content) < 11:
            return self.content
        return '{}...'.format(self.content[:10])


class Reply(models.Model):
    question = models.ForeignKey(Question)
    tutor = models.ForeignKey(Tutor)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "question : {}  user : {}".format(self.question.content[:10], self.tutor.user.name)

    def content_summary(self):
        if len(self.content) < 11:
            return self.content
        return '{}...'.format(self.content[:10])
