from flask import Flask, render_template, json, request, redirect
import database.db_connector as db
import os
from datetime import datetime

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
        return render_template("aircraft/aircraft_parts.j2", ac_parts=ac_parts, parts_list=all_parts, ac=aircraft_id)

    if request.method == "POST":
        pn = request.form["searchUpdate"]
        add_part_query = 'INSERT INTO aircraft_parts VALUES ("' + aircraft_id + '", "' + pn + '");'
        cur = db.execute_query(db_connection=db_connection, query=add_part_query)
        return redirect('/aircraft/parts/' + aircraft_id)

@app.route('/aircraft/parts/<string:aircraft_id>/<string:pn>', methods=['POST', 'GET'])
def del_aircraft_parts(aircraft_id, pn):
    if request.method == "GET":
        return render_template("aircraft/delete_part.j2", aircraft_id=aircraft_id, pn=pn)
    
    if request.method =="POST":
        del_query = 'DELETE FROM aircraft_parts WHERE id_aircraft = "' + aircraft_id + '" AND part_number = "' + pn + '"'
        cur = db.execute_query(db_connection=db_connection, query=del_query)
        return redirect('/aircraft/parts/' + aircraft_id)

@app.route('/repairs', methods=['POST', 'GET'])
def repairs_page():
    if request.method == "GET":
        repairs_query = "SELECT * FROM repairs;"
        cur = db.execute_query(db_connection=db_connection, query=repairs_query)
        repairs_table = cur.fetchall()
        return render_template("repairs/repairs.j2", repairs=repairs_table)
    
@app.route('/repairs/create', methods=['POST', 'GET'])
def add_repair():
    if request.method == "GET":
        removal_id_query = "SELECT id_removal FROM removals;"
        cur = db.execute_query(db_connection=db_connection, query=removal_id_query)
        removal_ids = cur.fetchall()
        return render_template("repairs/add_repair.j2", removal_ids=removal_ids)

    if request.method == "POST":
        removal_id = request.form['removal_id']
        supplier = request.form['supplier']
        price = request.form['price']
        recieved = datetime.today().strftime('%Y-%m-%d')
        add_repair_query = 'INSERT INTO repairs (recieved, id_removal, supplier, price) VALUES ("' + recieved + '", "' + removal_id + '", "' + supplier + '", "' + price + '");'
        if removal_id != "" and supplier != "":
            cur = db.execute_query(db_connection=db_connection, query=add_repair_query)
        return redirect('/repairs')

@app.route('/repairs/update/<string:repair_id>', methods=['POST', 'GET'])
def update_repair(repair_id):
    if request.method == "GET":
        removal_id_query = "SELECT id_removal FROM removals;"
        the_removal_query = "SELECT id_removal FROM repairs WHERE id_repair = " + repair_id + ";"
        the_recieved_query = "SELECT recieved FROM repairs WHERE id_repair = " + repair_id + ";"
        the_supplier_query = "SELECT supplier FROM repairs WHERE id_repair = " + repair_id + ";"
        the_price_query = "SELECT price FROM repairs WHERE id_repair = " + repair_id + ";"
        the_completed_query = "SELECT completed FROM repairs WHERE id_repair = " + repair_id + ";"
        cur = db.execute_query(db_connection=db_connection, query=removal_id_query)
        removal_ids = cur.fetchall()
        cur = db.execute_query(db_connection=db_connection, query=the_removal_query)
        removal_id = cur.fetchone()
        cur = db.execute_query(db_connection=db_connection, query=the_recieved_query)
        recieved = cur.fetchone()['recieved']
        cur = db.execute_query(db_connection=db_connection, query=the_supplier_query)
        supplier = cur.fetchone()['supplier']
        cur = db.execute_query(db_connection=db_connection, query=the_price_query)
        price = cur.fetchone()['price']
        cur = db.execute_query(db_connection=db_connection, query=the_completed_query)
        completed = cur.fetchone()['completed']
        return render_template("repairs/update_repair.j2", 
        repair_id=repair_id, 
        removal_ids=removal_ids, 
        removal_id=removal_id,
        recieved=recieved,
        supplier=supplier,
        price=price,
        completed=completed)

    if request.method == "POST":
        removal_id = request.form["removal_id"]
        recieved = request.form["recieved"]
        supplier = request.form["supplier"]
        price = request.form["price"]
        completed = request.form["completed"]
        update_repair_query = 'UPDATE repairs SET recieved="' + recieved + '", supplier="' + supplier + '", price="' + price + '", completed="' + completed + '" WHERE id_repair="' + repair_id + '";'
        cur = db.execute_query(db_connection=db_connection, query=update_repair_query)
        return redirect('/repairs')

@app.route('/repairs/delete/<string:repair_id>', methods=['POST', 'GET'])
def delete_repair(repair_id):
    if request.method == "GET":
        delete_repair_query = 'SELECT repairs.id_removal, removals.removed_part FROM repairs INNER JOIN removals ON repairs.id_removal = removals.id_removal WHERE id_repair="' + repair_id + '";'
        cur = db.execute_query(db_connection=db_connection, query=delete_repair_query)
        delete_repair = cur.fetchall()
        removal_id = delete_repair[0]['id_removal']
        pn = delete_repair[0]['removed_part']
        return render_template("repairs/delete_repair.j2", repair_id=repair_id, removal_id=removal_id, pn=pn)
    
    if request.method == "POST":
        del_query = 'DELETE FROM repairs WHERE id_repair = "' + repair_id + '"'
        cur = db.execute_query(db_connection=db_connection, query=del_query)
        return redirect('/repairs')

@app.route('/removals', methods=['POST', 'GET'])
def removals_page():
    if request.method == "GET":
        removals_query = "SELECT * FROM removals;"
        cur = db.execute_query(db_connection=db_connection, query=removals_query)
        removals = cur.fetchall()
        return render_template("removals/removals.j2", removals=removals)

@app.route('/removals/part_detail/<string:pn>', methods=['POST', 'GET'])
def part_info_page(pn):
    if request.method == "GET":
        pn_query = 'SELECT * FROM parts WHERE part_number="' + pn + '";'
        cur = db.execute_query(db_connection=db_connection, query=pn_query)
        pn_info = cur.fetchall()
        nomenclature = pn_info[0]['name']
        description = pn_info[0]['description']
        return render_template("removals/part_detail.j2", pn=pn, nomenclature=nomenclature, description=description)

@app.route('/removals/create', methods=['POST', 'GET'])
def add_removal():
    if request.method == "GET":
        ac_query = "SELECT id_aircraft FROM aircraft;"
        pn_query = "SELECT part_number FROM parts;"
        cur = db.execute_query(db_connection=db_connection, query=ac_query)
        ac_ids = cur.fetchall()
        cur = db.execute_query(db_connection=db_connection, query=pn_query)
        pn_ids = cur.fetchall()
        rem_date = datetime.today().strftime('%Y-%m-%d')
        return render_template("removals/add_removal.j2", rem_date=rem_date, ac_ids=ac_ids, pn_ids=pn_ids)

    if request.method == "POST":
        removal_date = request.form['removed_date']
        ac_id = request.form['id_aircraft']
        rem_pn = request.form['rem_pn']
        add_removal_query = 'INSERT INTO removals (removal_date, id_aircraft, removed_part) VALUES ("' + removal_date + '", "' + ac_id + '", "' + rem_pn + '");'
        if removal_date != "" and ac_id != "" and rem_pn != "":
            cur = db.execute_query(db_connection=db_connection, query=add_removal_query)
        return redirect('/removals')

@app.route('/removals/update/<string:removal_id>', methods=['POST', 'GET'])
def update_removal(removal_id):
    if request.method == "GET":
        rem_info_query = 'SELECT id_removal, removal_date, removed_part, id_aircraft FROM removals WHERE id_removal = "' + removal_id + '";'
        cur = db.execute_query(db_connection=db_connection, query=rem_info_query)
        pn_query = "SELECT part_number FROM parts;"
        result = cur.fetchone()
        rem_date = result['removal_date']
        rem_pn = result['removed_part']
        ac_id = result['id_aircraft']
        cur = db.execute_query(db_connection=db_connection, query=pn_query)
        pn_ids = cur.fetchall()
        return render_template("removals/update_removal.j2", removal_id=removal_id, rem_date=rem_date, rem_pn=rem_pn, ac_id=ac_id, pn_ids=pn_ids)

    if request.method == "POST":
        inst_pn = request.form["inst_pn"]
        rep_date = request.form["inst_date"]
        update_removal_query = 'UPDATE removals SET installed_part="' + inst_pn + '", replacement_date="' + rep_date + '" WHERE id_removal="' + removal_id + '";'
        cur = db.execute_query(db_connection=db_connection, query=update_removal_query)
        return redirect('/removals')


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 45435))
    app.run(port=port, debug=True)
