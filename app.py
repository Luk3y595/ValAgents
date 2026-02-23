from flask import Flask, g, render_template
import sqlite3

# Database Function
DATABASE = 'Database.db'

# Initialise App
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
