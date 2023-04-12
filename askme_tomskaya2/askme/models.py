from django.db import models
from django.contrib.auth.models import User

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'text': f'Text {i} ',
    } for i in range(12)
]

ANSWERS = [
    {
        'id': i,
        'text': f'Answer text {i}'
    }for i in range(10)
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField()


class Tag(models.Model):
    tag_name = models.CharField(max_length=25)


# class QuestionManager(models.Manager):
#     def in_rating_order(self):
#         queryset = self.get_queryset().annotate(
#             rating=self.likes()
#         )
#         return queryset.order_by('rating')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    @property
    def answers_count(self):
        return Answer.objects.filter(question=self).count()

    @property
    def likes(self):
        return QuestionLike.objects.filter(question=self).count()

    # objects = QuestionManager()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    @property
    def likes(self):
        return AnswerLike.objects.filter(answer=self).count()


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)