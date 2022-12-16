from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from QLKS import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    USER = 1
    EMPLOYEE = 2
    ADMIN = 3


class CusRole(UserEnum):
    local = 1
    foreign = 2


class Gender(UserEnum):
    male = 1
    female = 2


class RoomType(UserEnum):
    normal = 1
    vip = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


bookRoom_cus = db.Table('bookRoom_cus',
                            Column('book_room_id', Integer, ForeignKey('book_room.id'), primary_key=True),
                            Column('customer_id', Integer, ForeignKey('customer.id'), primary_key=True))


bookRoom_room = db.Table('bookRoom_room',
                            Column('book_room_id', Integer, ForeignKey('book_room.id'), primary_key=True),
                            Column('room_id', Integer, ForeignKey('room.id'), primary_key=True))


rent_cus = db.Table('rent_cus',
                            Column('rent_id', Integer, ForeignKey('rent.id'), primary_key=True),
                            Column('customer_id', Integer, ForeignKey('customer.id'), primary_key=True))


rent_room = db.Table('rent_room',
                            Column('rent_id', Integer, ForeignKey('rent.id'), primary_key=True),
                            Column('room_id', Integer, ForeignKey('room.id'), primary_key=True))


class Rent(BaseModel):
    __tablename__ = 'rent'
    checkInDate = Column(Date, default=datetime.now())
    checkOutDate = Column(Date)
    created_date = Column(Date, default=datetime.now())
    Orders = relationship('Order', backref='rent_order', uselist=False, lazy=True)
    status = Column(Boolean, default=True)

    rooms = relationship('Room', secondary=rent_room, lazy='subquery', backref=backref('rent', lazy=True))
    customers = relationship('Customer', secondary=rent_cus, lazy='subquery', backref=backref('rent', lazy=True))
    # customers = relationship('Customer', backref='customer_rent', lazy=True)
    # rooms = relationship('Room', backref='room_rent', lazy=True)

    def __str__(self):
        return str(self.id)


class BookRoom(BaseModel):
    __tablename__ = 'book_room'
    checkInDate = Column(Date)
    checkOutDate = Column(Date)
    created_date = Column(Date, default=datetime.now())
    status = Column(Boolean, default=True)

    rooms = relationship('Room', secondary=bookRoom_room, lazy='subquery', backref=backref('book_room', lazy=True))
    customers = relationship('Customer', secondary=bookRoom_cus, lazy='subquery', backref=backref('book_room', lazy=True))
    # customers = relationship('Customer', backref='customer', lazy=True)
    # rooms = relationship('Room', backref='room_book', lazy=True)

    def __str__(self):
        return str(self.id)


room_unit_room = db.Table('room_unit_room',
                            Column('room_id', Integer, ForeignKey('room.id'), primary_key=True),
                            Column('unit_room_id', Integer, ForeignKey('unit_room.id'), primary_key=True))


class Room(BaseModel):

    roomType = Column(Enum(RoomType), default=RoomType.normal)
    image = Column(String(100))
    description = Column(String(255))
    status = Column(Boolean, default=True)

    unit_rooms = relationship('unit_room', secondary=room_unit_room, lazy='subquery', backref=backref('room', lazy=True))
    book_room_id = Column(Integer, ForeignKey(BookRoom.id))
    rent_id = Column(Integer, ForeignKey(Rent.id))

    likes = relationship('like', backref='room', lazy=True)

    def __str__(self):
        return str(self.id)


class unit_room(BaseModel):

    __tablename__ = 'unit_room'
    unit = Column(String(255), nullable=False)
    unitPrice = Column(Float, nullable=True)

    def __str__(self):
        return self.unit


class User(BaseModel, UserMixin):

    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(50))
    gender = Column(Enum(Gender), default=Gender.male)
    joined_date = Column(Date, default=datetime.now())
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    orders = relationship('Order', backref='employee', lazy=True)
    customer = relationship('Customer', backref='user', uselist=False, lazy=True)

    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Customer(BaseModel):
    cus_role = Column(Enum(CusRole), default=CusRole.local)
    identity_card = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    book_room_id = Column(Integer, ForeignKey(BookRoom.id))
    rent_id = Column(Integer, ForeignKey(Rent.id))

    likes = relationship('like', backref='customer', lazy=True)

    def __str__(self):
        return self.user.name


class like(BaseModel):
    active = Column(Integer, default=1)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)


order_product = db.Table('order_product',
                            Column('order_id', Integer, ForeignKey('order.id'), primary_key=True),
                            Column('product_id', Integer, ForeignKey('product.id'), primary_key=True))


class surcharge(BaseModel):
    __tablename__ = 'surcharge'
    name = Column(String(100))
    surcharge = Column(Float)
    orders = relationship('Order', backref='surcharge', lazy=True)

    def __str__(self):
        return self.name


class Order(BaseModel):
    createdDate = Column(Date, default=datetime.now())
    totalPrice = Column(Float)
    rent_id = Column(Integer, ForeignKey(Rent.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    products = relationship('Product', secondary=order_product, lazy='subquery', backref=backref('orders', lazy=True))
    pay = Column(Boolean, default=False)
    surcharge_id = Column(Integer, ForeignKey(surcharge.id), nullable=False)

    def __str__(self):
        return self.id


class Category(BaseModel):
    name = Column(String(50), nullable=False)
    createdDate = Column(Date, default=datetime.now())
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = Column(String(50), nullable=False)
    number = Column(Integer)
    image = Column(String(100))
    unitPrice = Column(Float)
    createdDate = Column(Date, default=datetime.now())
    status = Column(Boolean, default=True)
    unit = Column(String(50), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    __tablename__ = 'comment'
    customer_id = Column(Integer, ForeignKey(User.id))
    cus_comment = Column(String(50))
    content_comment = Column(String(180))
    star_comment = Column(Integer)

    def __str__(self):
        return self.id


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib
        # password = str(hashlib.md5('123'.encode('utf-8')).hexdigest())
        #
        # u = User(name='Hoc', username='admin', password=password,
        #          avatar='https://res.cloudinary.com/duxlhasjq/image/upload/v1662007969/DangVanHoc_plm9kv.jpg',
        #          user_role=UserRole.ADMIN,
        #          gender=Gender.male,
        #          email='dangvanhoc1234@gmail.com',
        #          )
        # db.session.add(u)
        # db.session.commit()
