# Fellow Management System

Software Sustainability Institute internal tool to manager the Fellowship
program.

## Dependencies

~~~
$ sudo python3 -m pip install django
~~~

## Initialization

**Only run the following commands after you clone this repository
or when you pull new commits.**

~~~
$ ./bootstrap.sh
$ python3 manage.py migrate
~~~

## Super User

To create super user:

~~~
$ python3 manage.py createsuperuser
~~~

## Run

~~~
$ python3 manage.py runserver
~~~
