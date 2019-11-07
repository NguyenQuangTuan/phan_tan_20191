from functools import wraps
from phan_tan.common.errors import UPermissionDenied


def only(roles=[]):
    def verify_roles(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            def __allow_permission(roles_request, role_permissions):
                return set(role_params).intersection(role_permissions)

            self = args[0]
            role_params = self.jwt_data['roles']
            role_vals = [role.value for role in roles]

            if not __allow_permission(role_params, role_vals):
                raise UPermissionDenied

            return func(*args, **kwargs)

        return func_wrapper

    return verify_roles
