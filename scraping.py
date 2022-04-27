from datetime import datetime
from MyScripts.habr_search import HabrSearch

if __name__ == '__main__':
    start = datetime.now()
    habr = HabrSearch()
    habr.paginator()
    print(f'Всего найдено статей - {habr.result_count}.')
    print(f'Затрачено времени: {datetime.now() - start}')