from QLKS import db, model, app
from datetime import datetime
import hashlib


if __name__ == '__main__':
    with app.app_context():

        password = str(hashlib.md5('123'.encode('utf-8')).hexdigest())

        u1 = model.User(name="Hoc", username="vanhoc", password=password, user_role=model.UserRole.ADMIN,\
                         gender=model.Gender.male, joined_date=datetime.now(), phone='0962243787', email='dangvanhoc1234@gmail.com',\
                        avatar='https://res.cloudinary.com/duxlhasjq/image/upload/v1669512361/q7qycexa1k0pj7grlmdo.jpg')
        u2 = model.User(name="nobita", username="nobita", password=password, user_role=model.UserRole.EMPLOYEE, \
                        gender=model.Gender.male, joined_date=datetime.now(), phone='0962243787', email='nobita@gmail.com', \
                        avatar='https://res.cloudinary.com/duxlhasjq/image/upload/v1661421559/r3i8ynffssnqqcaduudj.png')
        u3 = model.User(name="doremon", username="doremon", password=password, user_role=model.UserRole.USER, \
                        gender=model.Gender.male, joined_date=datetime.now(), phone='0962243787', email='doremon@gmail.com', \
                        avatar='https://res.cloudinary.com/duxlhasjq/image/upload/v1641622531/k170rjkql7c6bdz3twnp.jpg')
        u4 = model.User(name="xuka", username="xuka", password=password, user_role=model.UserRole.USER, \
                        gender=model.Gender.female, joined_date=datetime.now(), phone='0962243787', email='xuka@gmail.com', \
                        avatar='https://res.cloudinary.com/duxlhasjq/image/upload/v1669512361/q7qycexa1k0pj7grlmdo.jpg')
        u5 = model.User(name="test", username="test", password=password, user_role=model.UserRole.USER, \
                        gender=model.Gender.male, joined_date=datetime.now(), phone='0962243787', email='test@gmail.com', \
                        avatar='https://res.cloudinary.com/duxlhasjq/image/upload/v1669512361/q7qycexa1k0pj7grlmdo.jpg')
        users = [u1, u2, u3, u4, u5]
        for u in users:
            db.session.add(u)
        db.session.commit()


        unit1 = model.unit_room(unit='hours-normalRoom', unitPrice=30000)
        unit2 = model.unit_room(unit='date-normalRoom', unitPrice=150000)
        unit3 = model.unit_room(unit='hours-vipRoom', unitPrice=50000)
        unit4 = model.unit_room(unit='date-vipRoom', unitPrice=300000)
        unitList = [unit1, unit2, unit3, unit4]
        for unit in unitList:
            db.session.add(unit)
        db.session.commit()


        r1 = model.Room(roomType=model.RoomType.normal, image="https://res.cloudinary.com/duxlhasjq/image/upload/v1670044539/room1_uwjsjh.jpg",\
                        description='Với chất lượng đạt chuẩn Quốc tế 4 sao,  Khách sạn Hoàng Sơn Peace không chỉ đáp ứng hoàn hảo.',\
                        unit_rooms=[unit1, unit2])
        r2 = model.Room(roomType=model.RoomType.vip,
                        image="https://res.cloudinary.com/duxlhasjq/image/upload/v1670044539/room6_qhsxo2.jpg", \
                        description='Với chất lượng đạt chuẩn Quốc tế 4 sao,  Khách sạn Hoàng Sơn Peace không chỉ đáp ứng hoàn hảo.',\
                        unit_rooms=[unit3, unit4])
        r3 = model.Room(roomType=model.RoomType.normal,
                        image="https://res.cloudinary.com/duxlhasjq/image/upload/v1670044539/room1_uwjsjh.jpg", \
                        description='Với chất lượng đạt chuẩn Quốc tế 4 sao,  Khách sạn Hoàng Sơn Peace không chỉ đáp ứng hoàn hảo.',\
                        unit_rooms=[unit1, unit2])
        r4 = model.Room(roomType=model.RoomType.vip,
                        image="https://res.cloudinary.com/duxlhasjq/image/upload/v1670044539/room6_qhsxo2.jpg", \
                        description='Với chất lượng đạt chuẩn Quốc tế 4 sao,  Khách sạn Hoàng Sơn Peace không chỉ đáp ứng hoàn hảo.',\
                        unit_rooms=[unit3, unit4])
        room = [r1, r2, r3, r4]
        for r in room:
            db.session.add(r)
        db.session.commit()

        cate1 = model.Category(name="bánh", createdDate=datetime.now())
        cate2 = model.Category(name="cơm", createdDate=datetime.now())
        cate3 = model.Category(name="nước giải khát", createdDate=datetime.now())

        category = [cate1, cate2, cate3]
        for cate in category:
            db.session.add(cate)
        db.session.commit()

        pro1 = model.Product(name='Bánh bao', number=50, image="https://res.cloudinary.com/duxlhasjq/image/upload/v1665043016/dgmxhzi5nalkvjbrcwjp.png",\
                             unitPrice=50000, createdDate=datetime.now(), unit='phần', category_id=1)
        pro2 = model.Product(name='Bánh mì que ', number=45,
                             image="https://res.cloudinary.com/don1bfybr/image/upload/v1660139074/Spring%20JAVA/banh_mi_que_fitapx.png", \
                             unitPrice=55000, createdDate=datetime.now(), unit='phần', category_id=1)
        pro3 = model.Product(name='Bánh cuốn', number=20,
                             image="https://res.cloudinary.com/don1bfybr/image/upload/v1660139073/Spring%20JAVA/banh_cuon_zyrrqm.jpg", \
                             unitPrice=30000, createdDate=datetime.now(), unit='phần', category_id=1)
        pro4 = model.Product(name='Cơm chiên', number=50,
                             image="https://res.cloudinary.com/duxlhasjq/image/upload/v1664090570/e2kpdkbtnovpocskfcqi.png", \
                             unitPrice=75000, createdDate=datetime.now(), unit='phần', category_id=2)
        pro5 = model.Product(name='Cơm trộn', number=50,
                             image="https://res.cloudinary.com/don1bfybr/image/upload/v1660378832/Spring%20JAVA/com_tron_fz1zpu.png", \
                             unitPrice=60000, createdDate=datetime.now(), unit='phần', category_id=2)
        pro6 = model.Product(name='Coca', number=70,
                             image="https://res.cloudinary.com/don1bfybr/image/upload/v1660139077/Spring%20JAVA/Coca_qmo7uo.jpg", \
                             unitPrice=30000, createdDate=datetime.now(), unit='phần', category_id=3)
        pro7 = model.Product(name='Trả tắc', number=100,
                             image="https://res.cloudinary.com/don1bfybr/image/upload/v1660379218/Spring%20JAVA/tra_tac_cwbpx8.png", \
                             unitPrice=25000, createdDate=datetime.now(), unit='phần', category_id=3)
        pro8 = model.Product(name='Trà đào', number=56,
                             image="https://res.cloudinary.com/don1bfybr/image/upload/v1660379180/Spring%20JAVA/tra_dao_md8vtr.png", \
                             unitPrice=35000, createdDate=datetime.now(), unit='phần', category_id=3)
        products = [pro1, pro2, pro3, pro4, pro5, pro6, pro7, pro8]
        for pr in products:
            db.session.add(pr)
        db.session.commit()


        cus1 = model.Customer(cus_role=model.CusRole.local, identity_card='212983479028', user_id=3)
        cus2 = model.Customer(cus_role=model.CusRole.foreign, identity_card='212983479028', user_id=4)
        cus3 = model.Customer(cus_role=model.CusRole.local, identity_card='212983479028', user_id=5)
        customer = [cus1, cus2, cus3]
        for cus in customer:
            db.session.add(cus)
        db.session.commit()

        book1 = model.BookRoom(checkInDate=datetime.now(), checkOutDate='2022-12-07', rooms=[r1,r2], customers=[cus1, cus2])
        book2 = model.BookRoom(checkInDate=datetime.now(), checkOutDate='2022-12-08', rooms=[r2], customers=[cus2, cus3])
        book3 = model.BookRoom(checkInDate=datetime.now(), checkOutDate='2022-12-09', rooms=[r3], customers=[cus2])
        book4 = model.BookRoom(checkInDate=datetime.now(), checkOutDate='2022-12-10', rooms=[r1], customers=[cus1])
        bookRoom = [book1, book2, book3, book4]
        for book in bookRoom:
            db.session.add(book)
        db.session.commit()

        rent1 = model.Rent(checkInDate='2022-12-12', checkOutDate='2022-12-15', rooms=[r1,r2], customers=[cus1,cus2])
        rent2 = model.Rent(checkInDate='2022-12-10', checkOutDate='2022-12-21', rooms=[r2], customers=[cus1])
        rent3 = model.Rent(checkInDate='2022-12-6', checkOutDate='2022-12-17', rooms=[r2,r3], customers=[cus3])
        rentList = [rent1, rent2, rent3]
        for rent in rentList:
            db.session.add(rent)
        db.session.commit()

        sur1 = model.surcharge(name='normal', surcharge=1)
        sur2 = model.surcharge(name='three_cus', surcharge=1.25)
        sur3 = model.surcharge(name='three_cus_foreign', surcharge=1.75)
        sur4 = model.surcharge(name='normal_foreign', surcharge=1.5)
        serList = [sur1, sur2, sur3, sur4]
        for sur in serList:
            db.session.add(sur)
        db.session.commit()

        order1 = model.Order(rent_id=1, user_id=2, totalPrice=350000, products=[pro1,pro2,pro6], surcharge_id=1)
        order2 = model.Order(rent_id=2, user_id=2, totalPrice=270000, products=[pro3,pro5], surcharge_id=3)
        order3 = model.Order(rent_id=3, user_id=2, totalPrice=560000, products=[pro5,pro7,pro8], surcharge_id=4)
        orderList = [order1, order2, order3]
        for order in orderList:
            db.session.add(order)
        db.session.commit()

