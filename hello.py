""" A simple demo setup for submitting installation-script diagnostic
information. """

import os
import time
from contextlib import closing
from sqlite3 import dbapi2 as sqlite3
from flask import (Flask, request, g, redirect, url_for, render_template, flash)


app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'log.db'),
    DEBUG=True,
    SECRET_KEY='d28ac59f-3d06-48b6-8932-65570a3c8c92'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    return rv


def init_db():
    """Initializes the database."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db


@app.before_request
def before_request():
    g.db = get_db()


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def show_reports():
    cur = g.db.execute('select * from log order by id desc')
    entries = cur.fetchall()
    print(entries[0])
    return render_template('show_report.html', log=entries)


@app.route('/report', methods=['POST'])
def add_entry():
    print(request.form)
    g.db.execute("insert into log (system, node, release, version, machine, processor, time) values (?, ?, ?, ?, ?, ?, ?)",
                 [request.form['system'], request.form['node'],
                  request.form['release'], request.form['version'],
                  request.form['machine'], request.form['processor'],
                  time.ctime()])
    g.db.commit()
    flash('Report added.')
    return redirect(url_for('show_reports'))

if __name__ == '__main__':
    app.run()
