from flask import abort, redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user


class RestrictMixin(ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
                )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('auth_view', next=request.url))


class MyUserView(RestrictMixin, ModelView):
    column_exclude_list = ['password_hash']
    column_searchable_list = ['email']
    column_filters = ['roles']

    can_create = False
    can_edit = False
    can_delete = False

    page_size = 50


class MyDishView(RestrictMixin, ModelView):
    column_searchable_list = ['title']
    column_filters = ['price']

    page_size = 50


class MyCategoryView(RestrictMixin, ModelView):
    column_searchable_list = ['title']
    column_filters = ['title']

    page_size = 50


class MyOrderView(RestrictMixin, ModelView):
    column_searchable_list = ['address', 'email']
    column_filters = ['total_sum', 'date', ]

    page_size = 50
