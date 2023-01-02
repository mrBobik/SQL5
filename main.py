import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, drop_tables, Publisher, Book, Shop, Stock, Sale
import json

db_host = '127.0.0.1'
db_port = '5432'
db_login = 'postgres'
db_pass = '12345678'
db_name = 'alchemy_db'

DSN = f'postgresql://{db_login}:{db_pass}@{db_host}:{db_port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

def auto_create_tables():
    with open('fixtures/tests_data.json', 'r') as fd:
        data = json.load(fd)
        print(data)
    for record in data:
        model = {'publisher': Publisher, 'shop': Shop, 'book': Book, 'stock': Stock, 'sale': Sale}[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
    session.close()


def publisher_sales():
    pub_name = input('Введите имя издателя: ')
    for i in session.query(Sale).join(Stock).join(Book).join(Book.publisher).filter(Publisher.name == pub_name).all():
        print(i)


if __name__ == '__main__':
    create_tables(engine)
    # drop_tables(engine)
    auto_create_tables()
    publisher_sales()
