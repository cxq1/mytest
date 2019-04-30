from .base import * #NOQA

DEBUG =True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea',
        'USER': 'root',
        'PASSWORD': 'qq123321',
        'HOST': 'localhost',
        'PORT': '3307',
    }
}
INSTALLED_APPS +=[
    'debug_toolbar',
    'pympler',
    'debug_toolbar_line_profiler',
]
MIDDLEWARE +=[
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
DEBUG_TOOLBAR_CONFIG ={
    'JQUERY_URL':'https://cdn.bootcss.com.jquery/3.3.1/jquery.min.js',
}
INTERNAL_IPS=['127.0.0.1']

DEBUG_TOOLBAR_PANELS=[
    'debug_toolbar_line_profiler.panel.ProfilingPanel',
]