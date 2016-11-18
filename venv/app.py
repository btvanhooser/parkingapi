from flask import Flask, jsonify, request
import os
import sqlite3
import dbSetup

def getListOfLots():
    connection = sqlite3.connect("parking_lot.db")
    cursor = connection.cursor()
    select_query = "SELECT id, lot_name FROM parking_lot_list"
    resultList = []
    for row in cursor.execute(select_query):
        tempD = {"id": row[0], "name": row[1]}
        resultList.append(tempD)
    connection.close()
    return resultList
    
# goal: get all rows and put into dictionaries based on highest capicity value (id: id)
def getSortedLotsFromDB():
    connection = sqlite3.connect("parking_lot.db")
    cursor = connection.cursor()
    select_query = "SELECT id, lot_name, high, medium, low FROM parking_lot_list"
    lowList = []
    mediumList = []
    highList = []
    for row in cursor.execute(select_query):
        tempD = {"id": row[0], "name": row[1]}
        if row[2] > row[3] and row[2] > row[4]:
            highList.append(tempD)
        elif row[4] > row[2] and row[4] > row[3]:
            lowList.append(tempD)
        else:
            mediumList.append(tempD)
    connection.close()
    return {"low":lowList, "medium":mediumList, "high":highList}

def getSpecificLot(id):
    connection = sqlite3.connect("parking_lot.db")
    cursor = connection.cursor()
    select_query = "SELECT * FROM parking_lot_list WHERE id = {}".format(id)
    for row in cursor.execute(select_query):
        return {"id": row[0], "name": row[1], "high": row[2], "medium": row[3], "low": row[4]}
    return "No lot with that ID found"
    
app = Flask(__name__)

@app.route('/getLot/<int:id>')
def get_lot(id):
    result = getSpecificLot(id)
    d = {"results": result}
    if result == "No lot with that ID found":
        return jsonify(d), 404
    return jsonify(d)
    
@app.route('/getLots')
def get_lots():
    tempList = getListOfLots()
    d = {"results": tempList}
    return jsonify(d)

@app.route('/getLotCapacity/<int:id>')
def get_lot_capacity(id):
    result = getSpecificLot(id)
    if result == "No lot with that ID found":
        return jsonify({"results": result}), 404
    if result["high"] > result["medium"] and result["high"] > result["low"]:
        return jsonify({"results": "high"})
    elif result["low"] > result["medium"] and result["low"] > result["high"]:
        return jsonify({"results": "low"})
    return jsonify({"results": "medium"})
    
@app.route('/getLotsByCapacity')
def get_all_capacity():
    tempD = getSortedLotsFromDB()
    result = {"results" : tempD}
    return jsonify(result)
        
@app.route('/updateLot', methods=["PUT"])
def update_lot():
    request_data = request.get_json()
    connection = sqlite3.connect("parking_lot.db")
    cursor = connection.cursor()
    select_query = "SELECT * FROM parking_lot_list WHERE lot_name = '{}'".format(request_data['name'])
    for row in cursor.execute(select_query):
        select_query = "SELECT {} FROM parking_lot_list WHERE lot_name = '{}'".format(request_data['capacityLevel'],request_data['name'])
        newValue = 0
        for row in cursor.execute(select_query):
            newValue = int(row[0])
        newValue = newValue + 1
        update_query = "UPDATE parking_lot_list SET {} = {} WHERE lot_name = '{}'".format(request_data['capacityLevel'], newValue, request_data['name'])
        cursor.execute(update_query)
        connection.commit()
        connection.close()
        return jsonify({"results": "Lot successfully updated"})
    connection.close();
    return jsonify({"results": "No lot with that name exists"}), 400
        
@app.route('/refreshTable')
def refresh_table():
    connection = sqlite3.connect("parking_lot.db")
    cursor = connection.cursor()
    select_query = "SELECT * FROM last_update WHERE last_date_modified = CURRENT_DATE"
    flag = True
    for row in cursor.execute(select_query):
        flag = False
    connection.close()
    
    if flag:
        dbSetup.getFreshTable()
        return jsonify({"results": "Table successfully refreshed"})
    return jsonify({"results": "Table is already refreshed"}), 202

port = int(os.getenv('PORT', 8080))
host = os.getenv('IP', '0.0.0.0')

app.run(host=host, port=port)