from flask import Flask, render_template, json, request, redirect
import database.db_connector as db
import os

# Configuration
app = Flask(__name__)

db_connection = db.connect_to_database()

# Routes 
@app.route('/')
def root():
    return render_template("index.j2")

@app.route('/aircraft', methods=['POST', 'GET'])
def aircraft_page():
    if request.method == "GET":
        ac_query = "SELECT * FROM aircraft;"
        cur = db.execute_query(db_connection=db_connection, query=ac_query)
        ac_table = cur.fetchall()
        return render_template("aircraft/aircraft.j2", aircraft=ac_table)
    

@app.route('/aircraft/create', methods=['POST', 'GET'])
def add_aircraft():
    if request.method == "GET":
        return render_template("aircraft/add_aircraft.j2")

    if request.method == "POST":
        aircraftID = request.form['aircraftID']
        model = request.form['model']
        add_ac_query = 'INSERT INTO aircraft (id_aircraft, model) VALUES ("' + aircraftID + '", "' + model + '");'
        if aircraftID != "" and model != "":
            cur = db.execute_query(db_connection=db_connection, query=add_ac_query)
        return redirect('/aircraft')

@app.route('/aircraft/delete/<string:aircraft_id>', methods=['POST', 'GET'])
def delete_aircraft(aircraft_id):
    if request.method == "GET":
        fetch_ac_query = 'SELECT * FROM aircraft WHERE id_aircraft="' + aircraft_id + '"'
        cur = db.execute_query(db_connection=db_connection, query=fetch_ac_query)
        result = cur.fetchall()
        ac_id = result[0]["id_aircraft"]
        model = result[0]["model"]
        return render_template("aircraft/delete_aircraft.j2", aircraft_id=ac_id, model=model)
    
    if request.method == "POST":
        del_query = 'DELETE FROM aircraft WHERE id_aircraft = "' + aircraft_id + '"'
        cur = db.execute_query(db_connection=db_connection, query=del_query)
        return redirect('/aircraft')

@app.route('/aircraft/parts/<string:aircraft_id>', methods=['POST', 'GET'])
def aircraft_parts(aircraft_id):
    if request.method == "GET":
        ac_parts_query = 'SELECT aircraft_parts.part_number, parts.name, parts.description FROM aircraft_parts INNER JOIN parts ON aircraft_parts.part_number = parts.part_number WHERE aircraft_parts.id_aircraft="' + aircraft_id + '";'
        all_parts_query = 'SELECT part_number FROM parts;'
        cur = db.execute_query(db_connection=db_connection, query=ac_parts_query)
        ac_parts = cur.fetchall()
        cur = db.execute_query(db_connection=db_connection, query=all_parts_query)
        all_parts = cur.fetchall()
        return render_template("aircraft/aircraft_parts.j2", ac_parts=ac_parts, parts_list=all_parts)

    if request.method == "POST":
        pn = request.form["searchUpdate"]
        add_part_query = 'INSERT INTO aircraft_parts VALUES ("' + aircraft_id + '", "' + pn + '");'
        cur = db.execute_query(db_connection=db_connection, query=add_part_query)
        return redirect('/aircraft/parts/' + aircraft_id)

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 45434))
    app.run(port=port, debug=True)
