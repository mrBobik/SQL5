import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
    # book = relationship(Book, back_populates='publisher')

    def __str__(self):
        return f'{self.id}: {self.name}'


class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=80), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)
    publisher = relationship(Publisher, backref='book')

    def __str__(self):
        return f'{self.id}: {self.title}'


class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=True)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')

    def __str__(self):
        return f'{self.book} - {self.count}'


class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DATE, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref='stock')

    def __str__(self):
        # return f'{self.id}: {self.price} {self.date_sale} {self.count}'
        return f'{self.stock.book.title} | {self.stock.shop.name} | {self.price} | {self.date_sale}'


def create_tables(engine):
    Base.metadata.create_all(engine)


def drop_tables(engine):
    Base.metadata.drop_all(engine)

