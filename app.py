from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/createLot', methods=['POST'])
def create_lot():
    pass

@app.route('/getLot/<int:id>')
def get_lot(id):
    if id == 1:
        return 'Lot B'
    elif id == 2:
        return 'Lot M'
    else:
        return "I don't have that id"
    
@app.route('/getLots')
def get_lots():
    d = {'results': {'1':'Lot B', '2':'Lot M'}}
    return jsonify(d)

@app.route('/getLotCapacity/<int:id>')
def get_lot_capacity(id):
    if id == 1:
        return 'Mostly Full'
    elif id == 2:
        return 'Not quite full'
    else:
        return "I don't have that id"
    
port = int(os.getenv('PORT', 8080))
host = os.getenv('IP', '0.0.0.0')

app.run(host=host, port=port)