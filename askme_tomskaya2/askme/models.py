from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce

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


class QuestionManager(models.Manager):
    def in_rating_order(self):
        queryset = self.get_queryset()
        return queryset.order_by('-likes')


    def by_tag(self, tag_name):
        queryset = self.get_queryset()
        return queryset.filter(tags__tag_name__exact=tag_name)


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    likes = models.IntegerField()

    @property
    def answers_count(self):
        return self.answers.count()

    # @property
    # def likes(self):
    #     return QuestionLike.objects.filter(question=self).count()

    objects = QuestionManager()


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    likes = models.IntegerField()

    # @property
    # def likes(self):
    #     return AnswerLike.objects.filter(answer=self).count()


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField()


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField()


def new_user_(us):
    new_user = User.objects.create_user(username=us['username'], first_name=us['first_name'], last_name=us['last_name'],
                                      email=us['email'], password=us['password'])
    profile = Profile(user=new_user)
    profile.save()
    return new_user