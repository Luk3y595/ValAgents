"""Module providing a SQL version for use"""

import os
import sqlite3
from flask import Flask, g, render_template, request

# Database Function
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'ValAgents.db')

# Initialise App
app = Flask(__name__)


@app.route('/')
def home():
    """Function that is used to display all that is on the home page"""
    # home page - only shows name and id card
    sql = """
                SELECT
                    AgentInfo.agent_id,
                    AgentInfo.name,
                    Role.role,
                    AgentInfo.agent_id_card_img_url
                FROM AgentInfo
                JOIN Role ON Role.role_id=AgentInfo.role_id;
"""
    results = query_db(sql)
    return render_template('home.html', result=results)


@app.route('/agent.html')
def agent():
    """Function used to display all information about the selected agent"""
    agent_id = request.args.get('id')
    # agent page with all the info
    sql = """
            SELECT
                AgentInfo.agent_id,
                AgentInfo.name,
                Role.role,
                Flag.flag_img_url,
                BestMaps.best_maps,
                BestMaps.map_image_url,
                WorstMaps.worst_maps,
                WorstMaps.map_image_url,
                AgentInfo.signature_ability_one,
                AgentInfo.signature_ability_one_description,
                AgentInfo.ability_one,
                AgentInfo.ability_one_description,
                AgentInfo.ability_two,
                AgentInfo.ability_two_description,
                AgentInfo.ability_three,
                AgentInfo.ability_three_description,
                AgentInfo.ultimate,
                AgentInfo.ultimate_description,
                AgentInfo.country_of_origin,
                AgentInfo.ability_img_url,
                AgentInfo.ability_three_img_url,
                AgentInfo.ability_four_img_url,
                AgentInfo.ability_five_img_url,
                AgentInfo.ultimate_img_url,
                AgentInfo.fullart_img_id,
                AgentInfo.agent_description
            FROM AgentInfo
            JOIN Role ON Role.role_id=AgentInfo.role_id
            JOIN BestMaps ON BestMaps.best_map_id=AgentInfo.best_map_id
            JOIN WorstMaps ON WorstMaps.worst_map_id=AgentInfo.worst_map_id
            JOIN Flag ON Flag.flag_id=AgentInfo.flag_id
            WHERE AgentInfo.agent_id = ?
"""
    results = query_db(sql, (agent_id,), one=True)
    return render_template('agent.html', character=results)


@app.route('/duelist.html')
def duelist():
    """Function to show a page similar to home page
    but they only show the duelists"""
    # home page - duelists only - name and id card
    #role_id values are: 1 = Duelist, 2 = initiator, 3 = sentinel, 4 = controller
    sql = """
                SELECT
                    AgentInfo.agent_id,
                    AgentInfo.name,
                    Role.role,
                    AgentInfo.agent_id_card_img_url
                FROM AgentInfo
                JOIN Role ON Role.role_id=AgentInfo.role_id
                WHERE AgentInfo.role_id = '1';
"""
    results = query_db(sql)
    return render_template('duelist.html', duelist=results)


@app.route('/initiator.html')
def initiator():
    """Function to show a page similar to home page
        but they only show the initiators"""
    # home page - initiator only - name and id card
    sql = """
                SELECT
                    AgentInfo.agent_id,
                    AgentInfo.name,
                    Role.role,
                    AgentInfo.agent_id_card_img_url
                FROM AgentInfo
                JOIN Role ON Role.role_id=AgentInfo.role_id
                WHERE AgentInfo.role_id = '2';
"""
    results = query_db(sql)
    return render_template('initiator.html', initiator=results)


@app.route('/sentinel.html')
def sentinel():
    """Function to show a page similar to home page
        but they only show the sentinels"""
    # home page - sentinel only - name and id card
    sql = """
                SELECT
                    AgentInfo.agent_id,
                    AgentInfo.name,
                    Role.role,
                    AgentInfo.agent_id_card_img_url
                FROM AgentInfo
                JOIN Role ON Role.role_id=AgentInfo.role_id
                WHERE AgentInfo.role_id = '3';
"""
    results = query_db(sql)
    return render_template('sentinel.html', sentinel=results)


@app.route('/controller.html')
def controller():
    """Function to show a page similar to home page
        but they only show the controllers"""
    # home page - controller only - name and id card
    sql = """
                SELECT
                    AgentInfo.agent_id,
                    AgentInfo.name,
                    Role.role,
                    AgentInfo.agent_id_card_img_url
                FROM AgentInfo
                JOIN Role ON Role.role_id=AgentInfo.role_id
                WHERE AgentInfo.role_id = '4';
"""
    results = query_db(sql)
    return render_template('controller.html', controller=results)


def get_db():
    """Function used to connect and retrieve
    the information from the database which is then shown to the user"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(_exception):
    """Function used to disconnect SQLite database connection
    at the end of the request"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """Function used to run SQL query, fetch the results,
    close the cursor, and return all the rows or just one row"""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


if __name__ == '__main__':
    app.run(debug=True)
