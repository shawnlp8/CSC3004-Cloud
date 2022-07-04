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

@app.route('/searchItem', methods = ["GET"])
def searchItem():
    if (request.method == "GET"):
        item = request.form.get("item")
        searchItemHelper(item)

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

@app.route('/updateSupermarket', methods = ["PUT"])
def updateSupermarket(supermarketID, supermarketName, supermarketBranch, imageFileName):
    if (request.method == "updateSupermarket"):
        supermarketName = request.form.get("supermarketName")
        supermarketBranch = request.form.get("supermarketBranch")
        imageFileName = request.form.get("imageFileName")
        insertSupermarketHelper(supermarketName, supermarketBranch, supermarketAddress)
    return "Insert Successful!"
    
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

def insertSupermarketHelper(supermarketName, supermarketBranch, supermarketAddress):
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sqlStatementSupermarket = "INSERT INTO Supermarket (name,branch,address) VALUES (" + str(supermarketName) + ", " + str(supermarketBranch) + ", " + str(supermarketAddress) + ")"
    cursor.execute(sqlStatementSupermarket)
    sqlStatementPhysicalFP = "INSERT INTO PhysicalFP (supermarketID) VALUES (" + cursor.lastrowid + ")"
    cursor.execute(sqlStatementPhysicalFP)
    connection.commit()
    connection.close()

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

def updateSupermarketHelper(supermarketID, supermarketName, supermarketBranch, imageFileName):
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sql = ''' UPDATE tasks
              SET priority = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    sqlStatementUpdateSupermarket = "UPDATE Supermarket SET supermarketName = " + supermarketName + ", supermarketBranch = " + supermarketBranch + " WHERE supermarketID = " + supermarketID
    cursor.execute(sqlStatementUpdateSupermarket)
    sqlStatementUpdatePhysicalFP = "UPDATE PhysicalFP SET imageFileName = " + imageFileName + " WHERE supermarketID = " + supermarketID
    cursor.execute(sqlStatementUpdatePhysicalFP)
    connection.commit()
    if not (cursor.rowcount == 0):
        print(record)
        return "Update successful!"
    else:
        return "Update failed, please try again!"
    connection.close()
        

if __name__ == '__main__':
    # Run the Flask server
    print("\nFlask server started and listening on port 5000...\n")
    app.run(debug=True)
    
    