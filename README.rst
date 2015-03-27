=============================
django-bower-cdn
=============================


Automatic add CDN for your local django-bower installed libs.

.. DANGER::
   This lib is not production ready yet.


Documentation
-------------

The full documentation is at https://django-bower-cdn.readthedocs.org.

Quickstart
----------

Install django-bower-cdn::

    pip install django-bower-cdn

Install and configure django-bower from https://github.com/nvbn/django-bower/

Add django-bower-cdn to `INSTALLED_APPS` in your settings:

.. code-block:: python

   'cdn_js',

Add staticfinder to `STATICFILES_FINDERS`:

.. code-block:: python

    'cdn_js.finders.CDNFinder',

Add a backend to your settings:

.. code-block:: python

    CDN_BACKEND = 'cdn_js.backends.cdn_jsdelivr'

Now instead of using staticfiles on your templates use:

.. code-block:: django

  {% load cdn %}

  {% cdn_static 'bootstrap/dist/js/bootstrap.js' %}

When possible your assets will be linked to the public CDN used as backend on settings when DEBUG is False.

Features
--------

* TODO
