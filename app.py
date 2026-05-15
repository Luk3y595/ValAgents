from flask import Flask, g, render_template
import sqlite3

# Database Function
DATABASE = 'ValAgents.db'

# Initialise App
app = Flask(__name__)


@app.route('/')
def home():
    # home page - shows only
    sql = """
                SELECT AgentInfo.agent_id,AgentInfo.name,Role.role,
                AgentInfo.agent_id_card_img_url
                FROM AgentInfo
                JOIN Role ON Role.role_id=AgentInfo.role_id;
"""
    results = query_db(sql)
    return render_template('home.html', result=results)


@app.route('/duelist.html')
def duelist():
    # home page - duelist only
    sql = """
                SELECT AgentInfo.agent_id,AgentInfo.name,Role.role,
                AgentInfo.agent_id_card_img_url
                FROM AgentInfo
                JOIN Role ON Role.role_id=AgentInfo.role_id
                WHERE AgentInfo.role_id = '1';
"""
    results = query_db(sql)
    return render_template('duelist.html', duelist=results)


@app.route('/initiator.html')
def initiator():
    # home page - initiator only
    sql = """
                SELECT AgentInfo.agent_id,AgentInfo.name,Role.role,
                AgentInfo.agent_id_card_img_url
                FROM AgentInfo
                JOIN Role ON Role.role_id=AgentInfo.role_id
                WHERE AgentInfo.role_id = '2';
"""
    results = query_db(sql)
    return render_template('initiator.html', initiator=results)


@app.route('/sentinel.html')
def sentinel():
    # home page - sentinel only
    sql = """
                SELECT AgentInfo.agent_id,AgentInfo.name,Role.role,
                AgentInfo.agent_id_card_img_url
                FROM AgentInfo
                JOIN Role ON Role.role_id=AgentInfo.role_id
                WHERE AgentInfo.role_id = '3';
"""
    results = query_db(sql)
    return render_template('sentinel.html', sentinel=results)


@app.route('/controller.html')
def controller():
    # home page - controller only
    sql = """
                SELECT AgentInfo.agent_id,AgentInfo.name,Role.role,
                AgentInfo.agent_id_card_img_url
                FROM AgentInfo
                JOIN Role ON Role.role_id=AgentInfo.role_id
                WHERE AgentInfo.role_id = '4';
"""
    results = query_db(sql)
    return render_template('controller.html', controller=results)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


if __name__ == '__main__':
    app.run(debug=True)
