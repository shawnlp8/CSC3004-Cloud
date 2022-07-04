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
    searchItemHelper()
    return render_template('index.html')

@app.route('/searchItem', methods = ["GET"])
def searchItem():
    if (request.method == "GET"):
        item = request.form.get("item")
        searchItemHelper(item)
        
# Helper functions
def searchItemHelper(item):
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sqlStatement = "SELECT * FROM Product WHERE name LIKE '%'" + str(item) + "'%'"
    cursor.execute(sqlStatement)
    record = cursor.fetchall()
    cursor.close()
    print(record)
    return record
        

if __name__ == '__main__':
    # Run the Flask server
    print("\nFlask server started and listening on port 5000...\n")
    app.run(debug=True)
    
    