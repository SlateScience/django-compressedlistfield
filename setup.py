import os
from distutils.core import Command
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import django
        from django.core.management import call_command
        from django.conf import settings

        settings.configure(
            DATABASES={'default': {
                'NAME': ':memory:',
                'ENGINE': 'django.db.backends.sqlite3'
            }},
            INSTALLED_APPS=(
                'django.contrib.contenttypes',
                'compressedlistfield.test_app.apps.TestConfig',
            )
        )

        django.setup()
        call_command('test', 'compressedlistfield')


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-compressedlistfield',
    version='0.1',
    packages=['compressedlistfield'],
    include_package_data=True,
    license='BSD License',
    description='A Django compressed list model field',
    long_description=README,
    url='https://github.com/SlateScience/django-compressedlistfield',
    author='Benny Daon',
    author_email='benny@slatescience.com',
    install_requires=['Django >= 1.8.0'],
    tests_require=['Django >= 1.8.0'],
    cmdclass={'test': TestCommand},
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
