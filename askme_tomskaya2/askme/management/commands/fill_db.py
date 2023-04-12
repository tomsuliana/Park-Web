# from django.core.management.base import BaseCommand
# from .models import Question, User
# from faker import Faker
# import random
#
#
# class Command(BaseCommand):
#     help = "filling databse with random data"
#     fake = Faker()
#
#     def create_fake_users(self, count):
#         print('users creation started')
#         words = list(set(self.fake.words(nb=10000)))
#         random.shuffle(words)
#         usernames = []
#         i = 0
#         while i < count:
#             for first_word in words:
#                 for second_word in words:
#                     usernames.append(first_word + second_word)
#                     i += 1
#         users = [User(username=usernames[i]],
#                     email = self.fake.email(),
#                     password = self.fake.password())
#                 for i in range(count)]
#
#         User.objects.bulk_create(users)
#         print('users done')
#     def create_fake_questions:
#         users = User.objects.all()
#
#         print('Start creating questions')
#         questions = [Question(title=self.fake.sentence(),
#                               text=self.fake.text(),
#                               user=random.choice(users))
#                      for _ in range(count)]
#
#         Question.objects.bulk_create(questions)
#
#         print('Questions are done')
