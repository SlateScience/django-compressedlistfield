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
        from django.conf import settings
        settings.configure(
            DATABASES={'default': {'NAME': ':memory:', 'ENGINE': 'django.db.backends.sqlite3'}},
            INSTALLED_APPS=('compressedlistfield', 'django.contrib.contenttypes')
        )
        from django.core.management import call_command
        import django

        if django.VERSION[:2] >= (1, 7):
            django.setup()
        call_command('test', 'compressedlistfield')


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-compressedlistfield',
    version='0.1',
    packages=['compressedlistfield'],
    include_package_data=True,
    license='BSD License',  # example license
    description='A Django app that prvides a compressed list field',
    long_description=README,
    url='https://github.com/SlateScience',
    author='BennyDaon',
    author_email='yourname@example.com',
    install_requires=['Django >= 1.8.0'],
    tests_require=['Django >= 1.8.0'],
    cmdclass={'test': TestCommand},
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
