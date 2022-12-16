from QLKS.model import User, UserRole, Product, Category, Order, Rent, BookRoom, Room, Customer
from QLKS import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request
from flask_login import logout_user, current_user, login_required
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class RoomView(AuthenticatedModelView):
    column_searchable_list = ['id']
    column_filters = ['id']
    can_view_details = True
    can_export = True
    column_export_list = ['id', 'price']
    column_exclude_list = ['image']
    column_labels = {
        'roomType': 'Loại phòng',
        'image': 'Ảnh',
        'price': 'Gía',
        'description': 'Mô tả',
        'status': 'Trạng thái',
        'book_room': 'Đã đặt',
        'rent_room': 'Đã thuê'
    }
    page_size = 4
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }


# class StatsView(AuthenticatedView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/stats.html')


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_product_by_cate()
        return self.render('admin/index.html', stats=stats)


class Profit_stats_view(BaseView):
    @expose('/')
    @login_required
    def index(self):
        month_year = request.args.get('month')
        month = None
        year = None
        temp = []
        if month_year:
            temp = month_year.split('-')
            month = temp[1]
            year = temp[0]
        return self.render('admin/profit_stats.html', stats=dao.stat_profit(month=month, year=year), \
                            total_profit = dao.get_total_bill_in_month(month=month, year=year),\
                            last_m_y=dao.get_last_month_in_bill())
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class Room_stats_view(BaseView):
    @expose('/')
    @login_required
    def index(self):
        month_year = request.args.get('month')
        month = None
        year = None
        temp = []
        if month_year:
            temp = month_year.split('-')
            month = temp[1]
            year = temp[0]
        return self.render('admin/room_stats.html', stats=dao.stats_room(month=month, year=year),\
                           last_m_y=dao.get_last_month_in_bill())
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class rule_change(BaseView):
    @expose('/')
    @login_required
    def index(self):

        return self.render('admin/rule_change.html')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


admin = Admin(app=app, name='Sting Home Stay', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(AuthenticatedModelView(User, db.session, name='Người dùng'))
admin.add_view(AuthenticatedModelView(Customer, db.session, name='KH'))
admin.add_view(RoomView(Room, db.session, name='Phòng'))
admin.add_view(AuthenticatedModelView(Order, db.session, name='Hóa đơn'))
admin.add_view(AuthenticatedModelView(BookRoom, db.session, name='Đặt phòng'))
admin.add_view(AuthenticatedModelView(Rent, db.session, name='Thuê phòng'))
admin.add_view(Profit_stats_view(name="Doanh thu", category="Thống kê"))
admin.add_view(Room_stats_view(name="Tần suất sử phòng", category="Thống kê"))
admin.add_view(rule_change(name="Thay đổi quy định", category="Thay đổi QD"))
# admin.add_view(StatsView(name='Thống kê - báo cáo'))

admin.add_view(LogoutView(name='Đăng xuất'))