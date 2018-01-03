Django User Extensions
----------------------

I anticipate regularly using a few common extensions to the standard
django.contrib.auth model, and seek to unify them here.

In particular:

google-recaptcha should prevent bot attempts to register users or alter
passwords

users should have timezones, to be collected during registration

Installation
-------------


Install

.. code:: bash
    $ pip install -r requirements.txt
    $ pip install ./

Add to your Django setup

.. code:: python

    INSTALLED_APPS = [ # ...
        'captcha',
        'user_extensions'

    #...
    ]

    TEMPLATES = [{ #...
        'DIRS': [ #...
                  os.path.join(BASE_DIR, 'user_extensions/templates')]
    # ...
    }

    MIDDLEWARE = [ # ...
        user_extensions.middleware.TimezoneMiddleware]

    # Google Recaptcha Integration
    NOCAPTCHA = True
    RECAPTCHA_PUBLIC_KEY = '???'
    RECAPTCHA_PRIVATE_KEY = '???'
