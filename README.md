# Fellow Management System

Software Sustainability Institute internal tool to manager the Fellowship
program.

## Dependencies

~~~
$ python3 -m pip install django
~~~

## Initialization

**Only run this command once or when you pull new commits.**

~~~
$ ./bootstrap.sh
$ python3 manage.py migrate
~~~

## Run

~~~
$ python3 manage.py runserver
~~~
