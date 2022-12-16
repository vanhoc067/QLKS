from QLKS.model import User, Category, Product, Room, BookRoom, Rent, Customer, UserRole, Order, like, Comment, rent_room,\
    unit_room, room_unit_room, rent_cus, bookRoom_cus, bookRoom_room, surcharge
from QLKS import db
from flask import jsonify
import json
import urllib.request
import urllib
import uuid
import requests
import hmac
import hashlib
from sqlalchemy import func, extract


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(name, email, gender, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, email=email, gender=gender, username=username.strip(), password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def load_categories():
    return Category.query.all()


# def load_products(category_id=None, kw=None):
#     query = Product.query
#
#     if category_id:
#         query = query.filter(Product.category_id.__eq__(category_id))
#
#     if kw:
#         query = query.filter(Product.name.contains(kw))
#
#     return query.all()


def load_room():
    return Room.query.all()


def load_product_by_cate(category_id=None):
    query = Product.query
    if category_id:
        query = query.filter(Product.category_id.__eq__(category_id))
    return query.all()


def get_room_by_id(room_id=None):
    # query = Room.query
    # if room_id:
    #     query = query.filter(Room.id.__eq__(room_id))
    # return query.all()
    return Room.query.get(room_id)


def get_book_room_by_id(book_room_id):
    return BookRoom.query.get(book_room_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def create_book_room(customers, rooms, checkInDate, checkOutDate):
    user = Customer.query.get(int(customers))
    ro = Room.query.get(int(rooms))
    br = BookRoom(customers=[user], rooms=[ro], checkInDate=checkInDate, checkOutDate=checkOutDate)
    try:
        db.session.add(br)
        db.session.commit()
    except Exception as ex:
        return jsonify({'code': 500,
                        'error_ms': str(ex)})
    return jsonify({'code': 200,
                    'error_ms': 'Tao thanh cong!!!'})


def load_book_room(book_room_id):
    query = BookRoom.query

    if book_room_id:
        query = query.filter(BookRoom.id.__eq__(book_room_id))

    return query.all()


def load_rent(rent_id):
    query = Rent.query

    if rent_id:
        query = query.filter(Rent.id.__eq__(rent_id))

    return query.all()


def get_rent_by_id(rent_id):
    return Rent.query.get(rent_id)


def create_rent(customer_id, room_id, checkInDate, checkOutDate):
    user = Customer.query.get(int(customer_id))
    ro = Room.query.get(int(room_id))
    r = Rent(customers=[user], rooms=[ro], checkInDate=checkInDate, checkOutDate=checkOutDate)
    try:
        db.session.add(r)
        db.session.commit()
    except Exception as ex:
        return jsonify({'code': 500,
                        'error_ms': str(ex)})
    return jsonify({'code': 200,
                    'error_ms': 'Tao thanh cong!!!'})


def check_role_for_render(user):

        if (user.user_role == UserRole.USER or user.user_role == UserRole.EMPLOYEE):
            return '/'
        elif user.user_role == UserRole.ADMIN:
            return '/admin'


def load_bill(order_id):
    query = Order.query

    if order_id:
        query = query.filter(Order.id.__eq__(order_id))

    return query.all()


def get_order_by_id(order_id):
    return Order.query.get(order_id)


def pay_bill_with_momo(bill_id, amount, re_url):
    # parameters send to MoMo get get payUrl
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    partnerCode = "MOMO"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    orderInfo = "Pay with MoMo"
    redirectUrl = re_url
    ipnUrl = "https://momo.vn"
    amount = str(amount)
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    autoCapture = True
    requestType = "captureWallet"
    extraData = ""  # pass empty value or Encode base64 JsonString

    # before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl&orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId&requestType=$requestType
    rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType

    # signature
    h = hmac.new(bytes(secretKey, 'UTF-8'), rawSignature.encode(), hashlib.sha256)
    signature = h.hexdigest()
    data = {
        'partnerCode': partnerCode,
        'partnerName': "Test",
        'storeId': "MomoTestStore",
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'redirectUrl': redirectUrl,
        'ipnUrl': ipnUrl,
        'lang': "vi",
        'autoCapture': autoCapture,
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    data = json.dumps(data)
    data = bytes(data, encoding='utf-8')
    clen = len(data)
    req = urllib.request.Request(endpoint, data=data, \
                                 headers={'Content-Type': 'application/json', \
                                          'Content-Length': clen, 'User-Agent': 'Mozilla/5.0'}, method='POST')
    try:
        f = urllib.request.urlopen(req)
        response = f.read()
        f.close()
        return json.loads(response)['payUrl']
    except Exception as e:
        print(e)
        return None


def pay_bill(id=None):
    if id:
        try:
            Order.query.filter_by(id=int(id)).update(dict(pay=True))
            db.session.commit()
            return True
        except:
            return False
    else:
        return False


def get_like_by_id(customer_id, room_id):
    # return like.query.get(room_id)
    query = like.query
    if customer_id:
        query = query.filter(like.customer_id.__eq__(customer_id))
    if room_id:
        query = query.filter(like.room_id.__eq__(room_id))
    return query.first()


def create_like(customer_id, room_id):
    l = like(customer_id=customer_id, room_id=room_id)
    try:
        db.session.add(l)
        db.session.commit()
    except Exception as ex:
        return jsonify({'code': 500,
                        'error_ms': str(ex)})
    return jsonify({'code': 200,
                    'error_ms': 'Tao thanh cong!!!'})


def update_like(like_id=None, active=None):

    if like_id:
        if active == 1:
            up = like.query.filter_by(id=int(like_id)).first()
            up.active = 0
            db.session.commit()
        else:
            up = like.query.filter_by(id=int(like_id)).first()
            up.active = 1
            db.session.commit()
        return True
    else:
        return False


def get_comment():
    return db.session.query(Comment.cus_comment,Comment.content_comment,Comment.star_comment).order_by(Comment.id.desc()).all()


def add_comment(cus_comment, content_comment, star_comment):
    c = Comment(cus_comment=cus_comment, content_comment=content_comment,star_comment=star_comment)

    db.session.add(c)
    db.session.commit()

    return c


def count_product_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
             .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
             .group_by(Category.id).order_by(Category.id).all()


def get_last_month_in_bill():
    last_month_in_bill = db.session.query(Rent.created_date).order_by(Rent.created_date.desc()).first()
    last_month = last_month_in_bill[0].strftime("%m")
    last_year = last_month_in_bill[0].strftime("%Y")
    return {'month': last_month, 'year': last_year}


def stat_profit(month=None, year=None):
    bills = db.session.query(Room.roomType, func.sum(unit_room.unitPrice), func.count(Room.id)) \
                    .join(rent_room, rent_room.c.room_id == Room.id) \
                    .join(Rent, Rent.id == rent_room.c.rent_id) \
                    .join(room_unit_room, room_unit_room.c.room_id == Room.id) \
                    .join(unit_room, unit_room.id == room_unit_room.c.unit_room_id) \
                    .group_by(Room.roomType)
    if not month or not year:
        tempe = get_last_month_in_bill()
        month = tempe.get('month')
        year = tempe.get('year')
    if month and year:
        if type(month) is not int and month is not None:
            month = int(month)
        if type(year) is not int and year is not None:
            year = int(year)
        bills = bills.filter(extract('month', Rent.created_date) == month, \
                                            extract('year', Rent.created_date) == year)
    if len(bills.all()) <= 0:
        return None
    return bills.all()


def get_total_bill_in_month(month=None, year=None):
    tempe = stat_profit(month, year)
    total_profit=0
    if tempe:
        for t in tempe:
            total_profit += t[1]
    return total_profit


def stats_room(month=None, year=None):
    med_unit = db.session.query(Room.id, func.sum(func.datediff(Rent.checkOutDate, Rent.checkInDate))) \
                                .join(rent_room, rent_room.c.room_id == Room.id) \
                                .join(Rent, Rent.id == rent_room.c.rent_id) \
                                .group_by(Room.id)
    if not month or not year:
        tempe = get_last_month_in_bill()
        month = tempe.get('month')
        year = tempe.get('year')
    if month and year:
        if type(month) is not int and month is not None:
            month = int(month)
        if type(year) is not int and year is not None:
            year = int(year)
        med_unit = med_unit.filter(extract('month', Rent.created_date) == month, \
                                    extract('year', Rent.created_date) == year)
    if len(med_unit.all()) <= 0:
        return None
    return med_unit.all()


def check_day(create_date, checkInDate):
    checkDay = db.session.query(func.datediff(checkInDate, create_date)).all()
    if checkDay[0][0] >= 28:
        return False
    else:
        return True


def count_cus(book_id):
    count = db.session.query(func.count(Customer.id)).join(bookRoom_cus, bookRoom_cus.c.customer_id == Customer.id)\
                                                     .join(BookRoom, BookRoom.id == bookRoom_cus.c.book_room_id)
    if book_id:
        count = count.filter(BookRoom.id.__eq__(int(book_id))).all()
    if count[0][0] > 3:
        return False
    else:
        return True


def get_surcharge_by_id(sur_id):
    return surcharge.query.get(sur_id)
