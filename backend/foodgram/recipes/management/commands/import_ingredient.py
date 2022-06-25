import codecs
import csv
import os

from django.core.management.base import BaseCommand

from foodgram.settings import STATIC_ROOT
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import ingredients from csv table'

    def handle(self, *args, **options):
        path = os.path.join(STATIC_ROOT, 'data/ingredients.csv')
        with codecs.open(path, encoding='utf-8') as f:
            reader = csv.reader(f)
            if Ingredient.objects.exists():
                return None
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0], measurement_unit=row[1])
                print(f'{row[0]} added')
