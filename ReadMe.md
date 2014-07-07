# QuasselPy

A web based search engine for a quassel database. Tested with Postgres and Sqlite, but should support anything SqlAlchemy can.

![](https://i.imgur.com/ay00toq.png)

# Installation

* Install [Python](https://www.python.org/downloads/)
* [Download](https://github.com/Zren/QuasselPy/archive/master.zip)/Clone this project.
* Run `./install.sh`
* Open `./config.py` and edit your database uri (default set to Sqlite on the current user).
* Run `run.sh` or `python app.py` and visit `http://localhost:5000/` in your browser.

# Uses

* [Python 2/3](https://www.python.org/downloads/)
    * [SqlAlchemy](http://www.sqlalchemy.org/)
    * [pg8000](https://github.com/mfenniak/pg8000) (Postgres)
    * [Flask](http://flask.pocoo.org/)
* [jQuery](https://jquery.com/)
* [jQuery.DataTables](http://datatables.net/)
* [Bootstrap 3](http://getbootstrap.com/)
