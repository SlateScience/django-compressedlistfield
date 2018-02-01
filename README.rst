==========================
django-compressedlistfield
==========================

django-compressedlistfield provides a Django model field which stores
a compressed, auto growing, list of integers.

It uses bz2 for compresing the list, but you don't have to worry about
it as it transparently takes care of serialization. To use, simply add the
field to one of your models.

Python 3 & Django 1.8 through 1.11 supported!

Installation
------------

.. code-block:: shell

    pip install django-compressedlistfield


Usage
-----

.. code-block:: python

    from django.db import models
    from compressedlistfield import CompressedListField

    class Achievement(models.Model):
      scores = CompressedListField()

Other Classes
-------------

**compressedlistfield.AutoGrowingList**

An extension of the builtin **list** that supports auto expansion and one
based indexing. Uses the **EMPTY** constant to mark empty cells and used by 
**CompressedListField** for the datastore.


Compatibility
--------------

django-compressedlist aims to support the same versions of Django currently
maintained by the main Django project. See `Django supported versions`_,
currently:

  * Django 1.8 (LTS) with Python 2.7, 3.3, 3.4, or 3.5
  * Django 1.11 (LTS) with Python 2.7, 3.4, 3.5 or 3.6
  * Django 2.0 with Python 3.4, 3.5 and 3.6

.. _Django supported versions: https://www.djangoproject.com/download/#supported-versions


Testing django-compressedlist Locally
-------------------------------------

To test against all supported versions of Django:

.. code-block:: shell

    $ docker-compose build && docker-compose up

Or just one version (for example Django 1.11 on Python 3.5):

.. code-block:: shell

    $ docker-compose build && docker-compose run tox tox -e py35-1.11

Or, you can create a virtualenv, install the django you want to test and run:

.. code-block:: shell

    $ python setup.py test
