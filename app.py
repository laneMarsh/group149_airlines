from flask import Flask, render_template, json
import database.db_connector as db
import os

# Configuration
app = Flask(__name__)

db_connection = db.connect_to_database()

# Routes 
@app.route('/')
def root():
    return render_template("index.j2")

@app.route('/aircraft')
def aircraft_page():
    query = "SELECT * FROM aircraft;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("aircraft.j2", aircraft=results)
    # return results

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    
    app.run(port=port, debug=True)