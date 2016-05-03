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

## Testing

If you want to test, follow the instructions:

~~~
$ python3 manage.py loaddata fixtures/demo.json
~~~

To export your changes on the database, run

~~~
$ python3 manage.py dumpdata --indent 4 fellowms > fixtures/demo.json
$ git commit -am 'Update database'
$ git push origin master
~~~
