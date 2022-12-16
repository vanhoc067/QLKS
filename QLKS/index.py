from flask import render_template, request, redirect, jsonify
from flask import session
from QLKS import app, dao, admin, login, utils
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from QLKS.decorators import anonymous_user
import cloudinary.uploader
import hashlib
import uuid


@app.route("/")
def index():
    # categories = dao.load_categories()
    # products = dao.load_products(category_id=request.args.get("category_id"),
    #                              kw=request.args.get('keyword'))
    # return render_template('index.html',
    #                        categories=categories,
    #                        products=products)
    comments = dao.get_comment()

    return render_template('index.html', comments=comments)


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


# @app.route('/products/<int:product_id>')
# def details(product_id):
#     p = dao.get_product_by_id(product_id)
#     return render_template('details.html', product=p)


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            try:
                dao.register(name=request.form['name'],
                             email=request.form['email'],
                             gender=request.form.get('gender'),
                             username=request.form['username'],
                             password=password,
                             avatar=avatar)

                return redirect('/login')
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
# @anonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            return redirect(dao.check_role_for_render(current_user))

    return render_template('login.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route('/room', methods=['get'])
def room():
    room = dao.load_room()

    return render_template('room.html', room=room)


@app.route('/api/room', methods=['post'])
@login_required
def create_book_room():
    data = request.json

    customers = data.get('customers')
    rooms = data.get('rooms')
    checkInDate = data.get('checkInDate')
    checkOutDate = data.get('checkOutDate')

    check = dao.check_day(create_date=datetime.now(), checkInDate=checkInDate)
    if check == False:
        return jsonify({'code': 400})
    else:
        final = dao.create_book_room(customers=customers, rooms=rooms, checkInDate=checkInDate,
                                     checkOutDate=checkOutDate)
        return jsonify({'code': 200})


@app.route('/room_detail/<int:room_id>/<int:customer_id>', methods=['get'])
def room_detail(room_id, customer_id):
    ro = dao.get_room_by_id(room_id=room_id)
    li = dao.get_like_by_id(customer_id=customer_id, room_id=room_id)

    test = {
        'checkInDate': datetime.now(),
        'checkOutDate': datetime.now(),
        'customer_id': 2,
        'room_id': 1
    }

    return render_template('room_detail.html', ro=ro, li=li)


@app.route('/products/<int:category_id>', methods=['get'])
def products(category_id):
    pro = dao.load_product_by_cate(category_id=category_id)

    return render_template('product.html', pro=pro)


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    data = request.json

    id = str(data['id'])
    name = data['name']
    price = data['price']

    key = app.config['CART_KEY']
    cart = session.get(key, {})

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/api/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)
    if cart and product_id in cart:
        quantity = int(request.json['quantity'])
        cart[product_id]['quantity'] = quantity

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)
    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/list_book_room', methods=['get'])
def list_book_room():
    book_room_id = request.args.get('book_room_id')
    list = dao.load_book_room(book_room_id=book_room_id)
    return render_template('list_book_room.html', list=list)


@app.route('/book_room_detail/<int:book_room_id>', methods=['get'])
def book_room_detail(book_room_id):
    br = dao.get_book_room_by_id(book_room_id=book_room_id)

    return render_template('book_room_detail.html', br=br)


@app.route('/list_rent', methods=['get'])
def list_rent():
    rent_id = request.args.get('rent_id')
    list = dao.load_rent(rent_id=rent_id)
    return render_template('list_rent.html', list=list)


@app.route('/rent_detail/<int:rent_id>', methods=['get'])
def rent_detail(rent_id):
    r = dao.get_rent_by_id(rent_id=rent_id)

    return render_template('rent_detail.html', r=r)


@app.route('/api/create_rent', methods=['post'])
@login_required
def create_rent():
    data = request.json

    customer_id = data.get('customer_id')
    room_id = data.get('room_id')
    checkInDate = data.get('checkInDate')
    checkOutDate = data.get('checkOutDate')
    book_id = data.get('book_id')

    if dao.count_cus(book_id=book_id) == False:
        return jsonify({'code': 400})
    else:
        final = dao.create_rent(customer_id=customer_id, room_id=room_id, checkInDate=checkInDate,
                                checkOutDate=checkOutDate)
        return jsonify({'code': 200})


@app.route('/list_bill', methods=['get'])
def list_bill():
    order_id = request.args.get('order_id')
    list = dao.load_bill(order_id=order_id)

    return render_template('list_bill.html', list=list)


@app.route('/order_detail/<int:order_id>', methods=['get'])
def order_detail(order_id):
    r = dao.get_order_by_id(order_id=order_id)
    rent = dao.get_rent_by_id(rent_id=r.rent_id)
    sur = dao.get_surcharge_by_id(r.surcharge_id)

    return render_template('order_detail.html', r=r, rent=rent, sur=sur)


@app.route('/api/pay-bill', methods=['post'])
@login_required
def pay():
    data = request.json
    id = data.get('id')
    if id:
        if dao.pay_bill(id):
            return jsonify({'code': 200})
    return jsonify({'code': 400})


@app.route('/api/momo_pay_status')
def get_momo_pay_status():
    data = request.json
    pass


@app.route('/api/pay_with_momo', methods=['post'])
@login_required
def pay_momo():
    data = request.json
    id = data.get('id')
    amount = data.get('amount')
    re_url = data.get('current_url')
    if id and amount and re_url:
        id = "Stay_Home_Hotel -" + str(id) + "-" + str(datetime.now())
        pay_url = dao.pay_bill_with_momo(bill_id=id, amount=amount, re_url=re_url)
        if pay_url:
            return jsonify({'code': 200, 'pay_url': pay_url})
    return jsonify({'code': 400})


@app.route('/api/create_like', methods=['post'])
@login_required
def create_like():
    data = request.json

    customer_id = data.get('customers')
    room_id = data.get('rooms')

    final = dao.create_like(customer_id=customer_id, room_id=room_id, )
    return final


@app.route('/api/like/<int:like_id>', methods=['put'])
def update_like(like_id):
    data = request.json
    active = data.get('active')
    if like_id:
        if dao.update_like(like_id=like_id, active=active):
            return jsonify({'code': 200})
    return jsonify({'code': 400})


@app.route('/api/comment', methods=['post'])
def add_comment():
    data = request.json
    content_comment = data.get('content_comment')
    cus_comment = data.get('cus_comment')
    star_comment = data.get('star_comment')

    try:
        c = dao.add_comment(cus_comment=cus_comment, content_comment=content_comment, star_comment=star_comment)
    except:
        return {'status': 404, 'err_msg': 'Chuong trinh bi loi'}

    return jsonify({'status': 201, 'comment': {
        'cus_comment': c.cus_comment,
        'content_comment': c.content_comment,
        'star_comment': c.star_comment
    }})


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_attributes():
    return {
        'cart': utils.cart_stats(session.get(app.config['CART_KEY']))
    }


if __name__ == '__main__':
    app.run(debug=True)
