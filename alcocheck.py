from sqlalchemy import and_

from database import db_set
from set_models import Products, Groups, Spirits


class AlcoAnalyzer:

    def __init__(self, group_code):
        self.session = db_set
        self.group_code = group_code
        self.results = None

    def get_parent_results(self, group_code):
        parent_query = (self.session.query(Groups.code).
                        filter(Groups.code == group_code).
                        cte(name="SubGroups", recursive=True))

        child_query = (self.session.query(Groups.code).
                       filter(Groups.parent_code == parent_query.c.code))
        union_query = parent_query.union(child_query)
        return union_query

    def get_final_results(self):
        parent_query = self.get_parent_results(self.group_code)

        final_query = (
            self.session
            .query(
                Products.markingofthegood,
                Products.name,
                Spirits.alcoholic_content,
                Groups.name.label("group_name")
            )
            .join(Spirits, Products.markingofthegood == Spirits.markingofthegood)
            .join(Groups, Products.group_code == Groups.code)
            .filter(
                and_(
                    Groups.code.in_(parent_query),
                    Spirits.alcoholic_content < 1,
                    Products.name.isnot(None)
                )
            )
            .order_by(Groups.name.desc())
        )
        self.results = final_query


def main():
    """
    Запуск анализа для проверки. Основной запуск из main.py
    :return:
    """
    analyzer = AlcoAnalyzer('20766')
    analyzer.get_final_results()
    for res in analyzer.results:
        print(res)


if __name__ == '__main__':
    main()
