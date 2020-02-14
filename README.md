[![PyPI](https://img.shields.io/pypi/v/django-sandstorm.svg)](https://pypi.python.org/pypi/django-sandstorm)

# django-sandstorm
Django package for helping integrate a Django app with sandstorm.io

To use: `pip install django-sandstorm`

It is HIGHLY recommended you make a separate sandstorm settings file for your
app. Whether or not you do, the following needs to go in your app settings for
integration with sandstorm to work:

1. Add `django_sandstorm` to `INSTALLED_APPS`

        INSTALLED_APPS = [
            ...
            'django_sandstorm',
        ]
        
1. Set `AUTHENTICATION_BACKENDS` to
`django.contrib.auth.backends.RemoteUserBackend`. This is Django's built in
backend for handling remote user authentication.

        AUTHENTICATION_BACKENDS = [
            'django.contrib.auth.backends.RemoteUserBackend',
        ]
        
1. Add `django_sandstorm.middleware.SandstormUserMiddleware` to 
`MIDDLEWARE_CLASSES`. This middleware extends
`django.contrib.auth.middleware.RemoteUserMiddleware` to add Sandstorm specific
handling for remote user information.

        MIDDLEWARE_CLASSES = [
            ...
            'django_sandstorm.middleware.SandstormUserMiddleware',
        ]
        
    By default, this middleware creates a user with the Sandstorm User ID as a
    username, sets the user `first_name` and `last_name` fields, and looks for
    a default "admin" permission from Sandstorm, granting staff and superuser
    status if it is found.
    
    Extend the `SandstormUserMiddleware` class to customize this behavior.

1. Add `django_sandstorm.middleware.SandstormPreCsrfViewMiddleware` before
`django.middleware.csrf.CsrfViewMiddleware` in `MIDDLEWARE_CLASSES`.

        MIDDLEWARE_CLASSES = [
            ...
            'django_sandstorm.middleware.SandstormPreCsrfViewMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            ...
        ]

    Django requires a `Referer` header to be set for CSRF protection to work.
    Sandstorm does not set this header, so the middleware is needed to add it.
