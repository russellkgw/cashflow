import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# Config
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'cashflow.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('CASHFLOW_SETTINGS', silent=True)


# Database
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_data():
    # db = get_db()
    # db.execute('insert into entries (title, text) values (?, ?)',[request.form['title'], request.form['text']])
    # db.commit()
    # import pdb; pdb.set_trace()
    flash('Data successfully added')
    return redirect(url_for('index'))


@app.route('/assumptions/')
def hello():
    db = get_db()
    cur = db.execute('select variable, value from assumptions order by id desc')
    assumptions = cur.fetchall()
    return render_template('assumptions.html', assumptions=assumptions)
