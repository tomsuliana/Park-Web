from django.core.management.base import BaseCommand
from askme.models import *
from faker import Faker
import random



class Command(BaseCommand):
    help = "filling databse with random data"
    fake = Faker()

    def create_fake_users(self, count):
        print('users creation started')
        words = list(set(self.fake.words(nb=10000)))
        random.shuffle(words)
        usernames = []
        i = 0
        while i < count:
            for first_word in words:
                for second_word in words:
                    usernames.append(first_word + second_word)
                    i += 1
        users = [User(username=usernames[i],
                    email = self.fake.email(),
                    password = self.fake.password())
                for i in range(count)]

        User.objects.bulk_create(users)
        print('users done')

    def create_fake_questions(self, count):
        users = User.objects.all()

        print('Start creating questions')
        questions = [Question(title=self.fake.sentence(),
                              text=self.fake.text(),
                              author=random.choice(users))
                     for _ in range(count)]

        Question.objects.bulk_create(questions)

        print('Questions are done')


    def create_fake_answers(self, count):
        users = User.objects.all()
        questions = Question.objects.all()
        print('Start creating answers')

        answers = [Answer(question=random.choice(questions),
                          text=self.fake.text(),
                          author=random.choice(users))
                    for _ in range(count)]

        Answer.objects.bulk_create(answers)

        print('Answers are done')


    def create_fake_tags(self, count):

        print('Start creating tags')

        words = list(set(self.fake.words(nb=10000)))
        random.shuffle(words)
        tag_names = []
        i = 0
        while i < count:
            for first_word in words:
                for second_word in words:
                    tag_names.append(first_word + second_word)
                    i += 1
        tags = [Tag(tag_name=tag_names[i]) for i in range(count)]

        Tag.objects.bulk_create(tags)
        print('Tags done')


    def like_questions(self, count):
        users = User.objects.all()
        questions = Question.objects.all()

        print ('Start liking questions')

        questionlikes = [QuestionLike(question=random.choice(questions),
                                      user=random.choice(users))
                         for _ in range(count)]

        QuestionLike.objects.bulk_create(questionlikes)

        print('Questions liked')


    def like_answers(self, count):
        users = User.objects.all()
        answers = Answer.objects.all()

        print ('Start liking answers')

        answerlikes = [AnswerLike(answer=random.choice(answers),
                                    user=random.choice(users))
                      for _ in range(count)]

        AnswerLike.objects.bulk_create(answerlikes)

        print('Answers liked')

    def put_tags_to_questions(self):
        tags = Tag.objects.all()

        print('Putting tags on questions')
        for question in Question.objects.all():
            tags_to_add = random.choices(tags, k=2)
            for tag in tags_to_add:
                question.tags.add(tag.id)
                question.save()

        print('Tags on questions are done')

    def create_likes_values(self):
        questionlikes = QuestionLike.objects.all()
        val_list = [-1, 0, 1]

        print('Start putting values to questionlikes')
        for questionlike in questionlikes:
            val = random.choice(val_list)
            questionlike.value = val
            questionlike.save()

        print('finished putting values')

        answerlikes = AnswerLike.objects.all()
        print('Start putting value to answerlikes')
        for answerlike in answerlikes:
            val = random.choice(val_list)
            answerlike.value = val
            answerlike.save()
        print('finished putting answerlike values')


    def create_likes_to_questions(self):
        # questionlikes = QuestionLike.objects.all()[:200]
        #
        # for questionlike in questionlikes:
        #     question = questionlike.question
        #     question.likes = question.likes + questionlike.value

        questions = Question.objects.all()
        print('Start counting question likes')

        for question in questions:
            for like in question.questionlike_set.all():
                question.likes = question.likes + like.value
                question.save()


        print('Finished counting question likes')


    def create_likes_to_answers(self):
        answers = Answer.objects.all()
        print('Start counting answer likes')

        for answer in answers:
            for like in answer.answerlike_set.all():
                answer.likes = answer.likes + like.value
                answer.save()


        print('Finished counting answer likes')



    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)


    def handle(self, *args, **options):
        ratio = options['ratio']

        users_count = ratio
        questions_count = ratio * 10
        answers_count = ratio * 100
        tags_count = ratio
        question_likes_count = ratio * 100
        answer_likes_count = ratio * 100

        # self.create_fake_users(users_count)
        # self.create_fake_questions(questions_count)
        # self.create_fake_answers(answers_count)
        # self.create_fake_tags(tags_count)
        # self.put_tags_to_questions()
        # self.like_questions(question_likes_count)
        # self.like_answers(answer_likes_count)
        # self.create_likes_values()
        # self.create_likes_to_questions()
        self.create_likes_to_answers()
