from io import StringIO
from urllib.request import urlopen

from django.contrib.auth import get_user_model
from django.core.management import CommandError, call_command
from django.db.models import Q
from django.test import TestCase

from blog.models import Post, Section

User = get_user_model()


class CommandTests(TestCase):
    """
    Тестирование кастомных команд для manage.py
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        User.objects.bulk_create(
            (User(id=1, username='1'), User(id=2, username='2'))
        )

        Section.objects.bulk_create(
            (Section(id=1, path='1', depth=1, numchild=2, slug='1'),
             Section(id=2, path='2', depth=2, numchild=2, slug='2'),
             Section(id=3, path='3', depth=2, numchild=1, slug='3'),
             Section(id=4, path='4', depth=3, numchild=0, slug='4'),
             Section(id=5, path='5', depth=3, numchild=0, slug='5'))
        )

    def test_api_available(self):
        """
        Проверяем, отвечает ли API сервиса рыбного текста.
        """

        url = 'https://fish-text.ru/get'

        with urlopen(url, timeout=5) as response:
            self.assertEqual(response.status, 200,
                             msg=f'API "{url}" не отвечает')

    def test_generate_posts_invalid_args(self):
        """
        Должно подняться исключение в случае запуска с невалидными аргументами:
          - переданы отрицательные значения в аргументы;
          - передан хоть один ID несуществующего автора;
          - передан хоть один ID несуществующего раздела.
        """

        with self.assertRaises(
                CommandError, msg='Приняты отрицательные значения аргументов'
        ):
            call_command('generate_posts', count=-1,
                         section_pks=-1, author_pks=-1)

        with self.assertRaises(CommandError,
                               msg='Приняты ключи несуществующих разделов'):
            call_command('generate_posts', count=1,
                         section_pks=(999, 1000), author_pks=(1, 2))

        with self.assertRaises(CommandError,
                               msg='Приняты ключи несуществующих авторов'):
            call_command('generate_posts', count=1,
                         section_pks=(4, 5), author_pks=(999, 1000))

    def test_generate_posts_valid_args(self):
        """
        Запустим команду с валидными аргументами. Должно создаться заданное
        количество постов с необходимыми атрибутами.
        """

        call_command('generate_posts', stdout=StringIO(), count=2,
                     section_pks=(4, 5), author_pks=(1, 2))

        created_posts_num = (Post.objects
                             .filter(picture='',
                                     status__in=Post.StatusChoices.values,
                                     author__in=(1, 2), section__in=(4, 5))
                             .exclude(Q(title='') | Q(slug='')
                                      | Q(content=''))
                             .count())

        self.assertEqual(created_posts_num, 2, msg='Посты не созданы')
