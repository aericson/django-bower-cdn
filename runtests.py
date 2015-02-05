import sys

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        MIDDLEWARE_CLASSES=[
        ],
        ROOT_URLCONF='cdn_js.urls',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'djangobower',
            'cdn_js',
        ],
        STATICFILES_FINDERS=(
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            'djangobower.finders.BowerFinder',
            'cdn_js.finders.CDNFinder',
        ),
        STATIC_URL='/static/',
        SITE_ID=1,
        NOSE_ARGS=['-s'],
        BOWER_INSTALLED_APPS=[
            'jquery#2.1.3'
        ],
        # TODO: use temporary folders
        BOWER_COMPONENTS_ROOT='tests/bower_components',
        STATIC_ROOT='tests/staticfiles',
        CDN_BACKEND='cdn_js.backends.cdn_jsdelivr',
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

    from django_nose import NoseTestSuiteRunner
except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
