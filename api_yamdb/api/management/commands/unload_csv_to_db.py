import csv
import os
import sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Загружает все данные из csv-файлов в static/data в БД'

    def handle(self, *args, **options):
        path_to_csv = os.path.abspath('static/data')

        connection = sqlite3.connect(os.path.abspath('db.sqlite3'))
        cursor = connection.cursor()

        for csv_file in os.listdir(path_to_csv):
            with open(os.path.abspath(f'static/data/{csv_file}'),
                      encoding='utf-8') as file:
                content = list(csv.reader(file, delimiter=","))
                column_names = ','.join(
                    [column_name for column_name in content[0]])
                values_len = ','.join(['?' for _ in range(len(content[0]))])
                insert_to = f'INSERT INTO {os.path(csv_file)}({column_names})'
                f'VALUES ({values_len})'
                cursor.executemany(insert_to, content[1:])

        connection.commit()
        connection.close()

        self.stdout.write(self.style.SUCCESS('Данные перенесены'))
