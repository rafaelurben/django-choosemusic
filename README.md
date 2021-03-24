# Choosemusic

Choosemusic is a Django app.

THIS IS TRASH, THAT'S WHY IT IS NOW ARCHIVED!

## Requirements

Django Admin is installed and activated.

## Quick start

1.  Add "choosemusic" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'choosemusic',
    ]

2.  Include the choosemusic URLconf in your project urls.py like this::

    path('choosemusic/', include('choosemusic.urls')),

3.  Run `python manage.py migrate` to create the models.

4.  Visit <http://127.0.0.1:8000/choosemusic/> and /admin/choosemusic
