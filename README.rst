Some Django User Extensions
---------------------------

I anticipate regularly needing a few common extensions to the standard
django.contrib.auth model.  They are unified here.

In particular:

* google-recaptcha should prevent bot attempts to register users or alter
passwords
* users can specify their timezones
* django context gets a user JWT

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
                  os.path.join(BASE_DIR, 'user_extensions/templates')
        #...
        ]

        'OPTIONS': {
            'context_processors': [ # ...
                'user_extensions.context_processors.add_jwt',
        #...
        ]
    # ...

    MIDDLEWARE = [ # ...
        'user_extensions.middleware.TimezoneMiddleware']

    USER_EXTENSIONS = {
        'JWT_TIMEOUT': timedelta(minutes=???), # pick a number
        'JWT_ALGORITHM': 'HS256'
    }

    # Google Recaptcha Integration
    NOCAPTCHA = True
    RECAPTCHA_PUBLIC_KEY = ???
    RECAPTCHA_PRIVATE_KEY = ???
