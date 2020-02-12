from urllib.parse import unquote

from django.contrib.auth.middleware import RemoteUserMiddleware
from django.utils.deprecation import MiddlewareMixin


class SandstormUserMiddleware(RemoteUserMiddleware):
    """
    Middleware for handling Sandstorm user properties.

    See: https://docs.sandstorm.io/en/latest/developing/auth/
    """
    header = "HTTP_X_SANDSTORM_USER_ID"
    user_full_name = 'HTTP_X_SANDSTORM_USERNAME'
    user_perms = 'HTTP_X_SANDSTORM_PERMISSIONS'

    def process_request(self, request):
        super().process_request(request)
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_original = request.user
            self.update_user_metadata(request)
            self.update_user_permissions(request)
            if request.user != user_original:
                request.user.save()

    def update_user_metadata(self, request):
        """
        Update metadata about the user based on Sandstorm headers.
        """
        # Set first and last name.
        if self.user_full_name in request.META:
            name = unquote(request.META.get(self.user_full_name))
            name_parts = name.split(' ')
            if hasattr(request.user, 'first_name'):
                request.user.first_name = name_parts[0]
            if hasattr(request.user, 'last_name') and len(name_parts) > 1:
                request.user.last_name = ' '.join(name_parts[1:])

    def update_user_permissions(self, request):
        """
        Update user permissions based on Sandstorm headers.

        This method assumes Sandstorm permissions matching the "staff" and
        "superuser" conventions in Django.
        """
        if self.user_perms in request.META:
            perms = request.META.get(self.user_perms).split(',')
            if 'staff' in perms:
                request.user.is_staff = True
            if 'superuser' in perms:
                request.user.is_superuser = True


class SandstormPreCsrfViewMiddleware(MiddlewareMixin):
    base_path = 'HTTP_X_SANDSTORM_BASE_PATH'
    referrer = 'HTTP_REFERER'

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if self.base_path in request.META:
            request.META[self.referrer] = request.META[self.base_path]
