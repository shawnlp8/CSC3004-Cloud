# Imports
import io
import csv
import random
import datetime
import os
from urllib import response
from flask import Flask, render_template, json, Response, redirect, redirect, jsonify, request, url_for
import sqlite3
from werkzeug.utils import secure_filename
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Manager')
def manager():
    db_Supermarket = getSupermarketHelper()
    
    #supermarketName = request.form.get("sName")
    #db_Branch = getBranchAJAX(supermarketName)
    db_Branch = getBranchAJAX()
    
    return render_template('Manager.html', db_Supermarket=db_Supermarket, db_Branch = db_Branch)

@app.route('/addSupermarket')
def addSuperMarket():
    return render_template('addSuperMarket.html')

@app.route('/Specifications')
def specifications():
    return render_template('product_specifications.html')

@app.route('/searchItem', methods = ["GET", "POST"])
def searchItem():
    request_data = request.get_json()
    # print("JSON String: \n", str(request_data))
    item = request_data['item']
    # print("item: " + item)
    return jsonify({'data': searchItemHelper(item)})

# Add new Supermarket
@app.route('/insertSupermarket', methods = ["POST"])
def insertSupermarket():
    if (request.method == "POST"):
        supermarketName = request.form.get("new_supermerket")
        supermarketBranch = request.form.get("new_Branch")
        supermarketAddress = request.form.get("new_Address")
        insertSupermarketHelper(supermarketName, supermarketBranch, supermarketAddress)
    return render_template('Manager.html')

@app.route('/insert_Blueprint', methods = ["POST"])
def insertBlueprint():
    if (request.method == "POST"):
        supermarketName = request.form.get("sName")
        supermarketBranch = request.form.get("bName")
        
        input_File = request.files['fName']
        if input_File.filename == '':
            return redirect(url_for('/Manager'))
        else:
            supermarketBlueprint = secure_filename(input_File.filename)

        insertPhysicalFPHelper(supermarketName, supermarketBranch, str(supermarketBlueprint))
        return render_template('product_specifications.html')
    
    
# Helper functions
def searchItemHelper(item):
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sqlStatement = "SELECT * FROM Product WHERE name LIKE '%" + str(item) + "%'"
    cursor.execute(sqlStatement)
    data = cursor.fetchall()
    if not (cursor.rowcount == 0):
        print(data)
        return data
    else:
        return "Item not found!"

def getSupermarketHelper():
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sqlStatement = "SELECT DISTINCT name FROM Supermarket"
    cursor.execute(sqlStatement)
    record = cursor.fetchall()
    if not (cursor.rowcount == 0):
        return record
    else:
        return "Cannot retrieve supermarket data, please try again!"

def getBranchAJAX():
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    #sqlStatement = "SELECT branch FROM Supermarket WHERE name='"+ supermarket +"'"
    sqlStatement = "SELECT DISTINCT branch FROM Supermarket"
    cursor.execute(sqlStatement)
    record = cursor.fetchall()
    if not (cursor.rowcount == 0):
        return record
    else:
        return "Cannot retrieve supermarket data, please try again!"

# Add new Supermarket Helper
def insertSupermarketHelper(supermarketName, supermarketBranch, supermarketAddress):
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sqlStatementSupermarket = "INSERT INTO Supermarket (name,branch,address) VALUES('"+ supermarketName +"', '"+ supermarketBranch +"', '"+ supermarketAddress +"')"
    cursor.execute(sqlStatementSupermarket)
    connection.commit()
    connection.close()

# Insert to PhysicalFP (Manager 1st page)
def insertPhysicalFPHelper(supermarket, branch, blueprint):
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sql_SupermarketID = "SELECT supermarketID FROM Supermarket WHERE name='"+ supermarket + "' AND branch='"+ branch +"'"
    cursor.execute(sql_SupermarketID)
    get_SupermarketID = cursor.fetchone()
    
    if not (cursor.rowcount == 0):
        sql_InsertPhysicalFP = "INSERT INTO PhysicalFP (supermarketID, imageFileName) VALUES(" + str(get_SupermarketID[0]) + ", '" + str(blueprint) +"')"
        cursor.execute(sql_InsertPhysicalFP)
        connection.commit()
        connection.close()
    else:
        return "No such Supermarket exists, please submit a new Supermarket."


if __name__ == '__main__':
    # Run the Flask server
    print("\nFlask server started and listening on port 5000...\n")
    app.run(debug=True)
    
    