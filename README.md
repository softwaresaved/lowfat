# Fellow Management System

Software Sustainability Institute internal tool to manager the Fellowship
program.

## Dependencies

- Python 3
- Django
- SQLite 3

### Dependencies Resolution on Debian and Ubuntu

~~~
$ sudo apt-get install python3 sqlite3
$ sudo python3 -m pip install -r requirements.txt
~~~

## Initialization

**Only run the following commands after you clone this repository
or when you pull new commits.**

Need to get CSS files and create local database.

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

## Development

### File System

- `bootstrap.sh`

  File to download CSS files.

- `db.sqlite3`

  Local database.

- `expenses/`

  Expense files used for test.

- `fellowms/`

  Django application root.

- `fixtures/`

  Data used when testing.

- `manage.py

  Django command line script.

- `photos/`

  Photos used for test.

- `README.md`

  Root of documentation.

- `requirements.txt`

  Python dependencies used by `pip`.
