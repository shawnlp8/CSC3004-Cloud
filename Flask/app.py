# Imports
import io
import csv
import random
import datetime
import os
from urllib import response
from flask import Flask, render_template, json, Response, redirect, redirect, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Manager')
def manager():
    return render_template('Manager.html')

@app.route('/Specifications')
def specifications():
    return render_template('product_specifications.html')

@app.route('/searchItem', methods = ["GET"])
def searchItem():
    if (request.method == "GET"):
        item = request.form.get("item")
        searchItemHelper(item)

# Add new Supermarket
@app.route('/insertSupermarket', methods = ["POST"])
def insertSupermarket():
    if (request.method == "POST"):
        supermarketName = request.form.get("supermarketName")
        supermarketBranch = request.form.get("supermarketBranch")
        supermarketAddress = request.form.get("supermarketAddress")
        insertSupermarketHelper(supermarketName, supermarketBranch, supermarketAddress)
    return "Insert Successful!"

@app.route('/getSupermarket', methods = ["GET"])
def getSupermarket():
    if (request.method == "GET"):
        getSupermarketHelper()

@app.route('/manager', methods = ["POST"])
def insertBlueprint():
    if (request.method == "POST"):
        supermarketName = request.form.get("supermarketName")
        supermarketBranch = request.form.get("supermarketBranch")
        supermarketBlueprint = request.form.get("supermarketBlueprint")

        reply = insertPhysicalFPHelper(supermarketName, supermarketBranch, supermarketBlueprint)
        return reply
    
    
# Helper functions
def searchItemHelper(item):
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sqlStatement = "SELECT * FROM Product WHERE name LIKE '%'" + str(item) + "'%'"
    cursor.execute(sqlStatement)
    record = cursor.fetchall()
    if not (cursor.rowcount == 0):
        print(record)
        return record
    else:
        return "Item not found!"

# Add new Supermarket Helper
def insertSupermarketHelper(supermarketName, supermarketBranch, supermarketAddress):
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sqlStatementSupermarket = "INSERT INTO Supermarket (name,branch,address) VALUES (" + str(supermarketName) + ", " + str(supermarketBranch) + ", " + str(supermarketAddress) + ")"
    cursor.execute(sqlStatementSupermarket)
    connection.commit()
    connection.close()

# Insert to PhysicalFP (Manager 1st page)
def insertPhysicalFPHelper(supermarket, branch, blueprint):
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sql_SupermarketID = "SELECT supermarketID FROM Supermarket WHERE name=" + supermarket + " AND branch=" + branch + ";"
    cursor.execute(sql_SupermarketID)
    get_SupermarketID = cursor.fetchall()
    
    if not (cursor.rowcount == 0):
        sql_InsertPhysicalFP = "INSERT INTO PhysicalFP (supermarketID, imageFileName) VALUES (" + int(get_SupermarketID) + ", " + str(blueprint) + ");"
        cursor.execute(sql_InsertPhysicalFP)
        connection.commit()
        connection.close()
    else:
        return "No such Supermarket exists, please submit a new Supermarket."

def getSupermarketHelper():
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sqlStatement = "SELECT * FROM Supermarket"
    cursor.execute(sqlStatement)
    record = cursor.fetchall()
    if not (cursor.rowcount == 0):
        print(record)
        return record
    else:
        return "Cannot retrieve supermarket data, please try again!"

    

if __name__ == '__main__':
    # Run the Flask server
    print("\nFlask server started and listening on port 5000...\n")
    app.run(debug=True)
    
    