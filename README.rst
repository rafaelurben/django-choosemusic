===========
Choosemusic
===========

Choosemusic is a Django app.

Quick start
-----------

1. Add "choosemusic" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'choosemusic',
    ]

2. Include the choosemusic URLconf in your project urls.py like this::

    path('choosemusic/', include('choosemusic.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/choosemusic/ to participate in the poll.
