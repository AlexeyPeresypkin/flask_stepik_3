from flask_admin.contrib.sqla import ModelView


class MyUserView(ModelView):

    column_exclude_list = ['password_hash']
    column_searchable_list = ['email']
    column_filters = ['role']

    can_create = False
    can_edit = False
    can_delete = False

    page_size = 50
