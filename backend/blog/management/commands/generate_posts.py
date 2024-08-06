from argparse import ArgumentTypeError
from collections import Counter
from json import loads as json_loads
from random import choice, randint
from textwrap import shorten
from typing import Any, Iterator
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from slugify import slugify

from blog.models import Post, Section

User = get_user_model()


def raise_on_false(func):
    """
    Декоратор. Райзит исключение, если функция проверки возвращает False.
    """

    def wrapper(value):
        value = int(value)
        if not func(value):
            raise ArgumentTypeError(f'"{value}" является'
                                    f' недопустимым значением')
        return value

    return wrapper


@raise_on_false
def is_positive(value: int):
    return value > 0


@raise_on_false
def is_section_exist(value):
    return Section.objects.filter(depth__gt=2, pk=value).exists()


@raise_on_false
def is_user_exist(value):
    return User.objects.filter(pk=value).exists()


class Command(BaseCommand):
    LOREM_URL = 'https://fish-text.ru/get'
    QUERY_PARAMS = {'number': 100, 'format': 'json'}
    AVAILABLE_CONTENT_TYPES = ('title', 'paragraph')

    help = ('Генерирует заданное количество бессмысленных постов. Необходимо'
            ' также указать, первичный(е) ключ(и) раздела(ов) и'
            ' пользователя(ей). Если передано несколько первичных ключей,'
            ' выбор связанной записи будет случайным. Все записи с переданными'
            ' первичными ключами должны существовать.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            '-c', '--count', type=is_positive, required=True,
            help='Количество постов'
        )
        parser.add_argument(
            '-s', '--section_pks', type=is_section_exist, required=True,
            nargs='+', help='Первичные ключи разделов для постов'
        )
        parser.add_argument(
            '-a', '--author_pks', type=is_user_exist, required=True, nargs='+',
            help='Первичные ключи пользователей-авторов'
        )

    def handle(self, *args, **options):
        random_lorem_data = self._get_data_for_posts(options['section_pks'],
                                                     options['author_pks'])

        self.stdout.write(self.style.NOTICE('Создаю посты в БД...'))
        Post.objects.bulk_create(
            (Post(**next(random_lorem_data)) for _ in range(options['count']))
        )

        self.stdout.write(self.style.SUCCESS('Готово!'))

    def _get_data_for_posts(
            self,
            section_pks: list[int] | tuple[int],
            author_pks: list[int] | tuple[int]
    ) -> Iterator[dict[str: Any]]:
        """
        Бесконечно (если сеть не отвалится) отдает словари с данными
        для создания рандомного поста.
        Ключи - имена полей, значения - значения полей.

        Принимает первичные ключи разделов постов и пользователей - авторов
        постов.

        - Разделы и авторы выбираются рандомно.
        - Контент для заголовков и содержимого берется по API сервиса с
          рыбными текстами.
        - Слаги генерируются на основе заголовка.
        - Аннотации генерируются из контента, но событие генерации рандомно.
        - Статус поста выбирается рандомно.
        - Картинки не генерируются из соображений места на диске.
        """

        titles = self._get_lorem_data('title')
        paragraphs = self._get_lorem_data('paragraph')
        existing_slugs = Counter(item.rstrip(' 0123456789') for item in
                                 Post.objects.values_list('slug', flat=True))
        bool_choices = (False, True)

        while True:
            data = {'content': next(paragraphs)}

            title = next(titles)
            slug = slugify(title)
            count = existing_slugs.get(slug, 0) + 1
            existing_slugs[slug] = count
            if count > 1:
                slug = f'{slug}-{count - 1}'

            data['title'] = title
            data['slug'] = slug
            data['annotation'] = (
                shorten(data['content'], randint(50, 100), placeholder='')
                if choice(bool_choices) else ''
            )
            data['status'] = choice(Post.StatusChoices.choices)[0]
            data['is_fixed'] = choice(bool_choices)
            data['author_id'] = choice(author_pks)
            data['section_id'] = choice(section_pks)

            yield data

    def _get_lorem_data(self, data_type: str) -> Iterator[str]:
        """
        Бесконечный итератор. Делает запрос к API, возвращает по одному
        элементу из полученных данных. Когда последовательность заканчивается,
        делает новый запрос.
        """

        assert data_type.lower() in self.AVAILABLE_CONTENT_TYPES, \
            (f'Недопустимый тип контента.'
             f' Возможные типы: {self.AVAILABLE_CONTENT_TYPES}')

        while True:
            self.stdout.write(
                self.style.NOTICE(f'Запрашиваю данные типа "{data_type}"')
            )
            yield from (
                self._fetch_lorem_data(
                    self.LOREM_URL, self.QUERY_PARAMS | {'type': data_type}
                )
                .removesuffix('\\n\\n')
                .split('\\n\\n')
            )

    def _fetch_lorem_data(self, url: str, query_params: dict[str, Any]) -> str:
        """
        Отправляет запрос на указанный адрес, извлекает данные, возвращает.
        """

        try:
            full_url = f'{url}?{urlencode(query_params)}'
            self.stdout.write(
                self.style.NOTICE(f'Посылаю запрос на "{full_url}"...')
            )
            with (urlopen(url + '?' + urlencode(query_params), timeout=5)
                  as response):
                data = json_loads(response.read().decode('utf-8'))

                if not ('status' in data and 'text' in data):
                    msg = (f'В ответе API нет необходимых ключей'
                           f'\nQUERY: {response.url}')
                    raise URLError(msg)

                if data['status'] != 'success':
                    raise URLError(data['text'])
        except URLError as e:
            self.stdout.write(
                self.style.ERROR(f'При обращении к API рыбного текста'
                                 f' произошел обосрамс\nПричина: "{e.reason}"')
            )
            raise SystemExit('Завершение работы программы')

        self.stdout.write(self.style.SUCCESS('Данные получены'))

        return data['text']
