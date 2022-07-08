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

global_Product = None
global_BP = None
global_Location = None

@app.route('/')
def index():
    """Returns the home page of the web application

    Returns:
    file: The web page that will be returned

   """
    return render_template('index.html')

@app.route('/Manager')
def manager():
    """Returns the manage page of the web application along with the neccessary data

    Returns:
    file: The web page that will be returned
    db_Supermarket: Dynamic supermarket data
    db_Branch: Dynamic branch data

   """
    db_Supermarket = getSupermarketHelper()
    db_Branch = getBranchAJAX()
    
    return render_template('Manager.html', db_Supermarket=db_Supermarket, db_Branch = db_Branch)

@app.route('/addSupermarket')
def addSuperMarket():
    """Returns the add supermarket page of the web application

    Returns:
    file: The web page that will be returned

   """
    return render_template('addSuperMarket.html')

@app.route('/Specifications', methods = ["GET", "POST"])
def specifications():
    """Returns the specifications of the web application

    Returns:
    file: The web page that will be returned

   """
    return render_template('product_specifications.html')

@app.route('/doneLabel', methods = ["POST"])
def doneLabel():
    """Returns the home page of the web application after a successful post request for label

    Returns:
    file: The web page that will be returned

   """
    if (request.method == "POST"):
        return render_template('index.html')

@app.route('/searchItem', methods = ["GET", "POST"])
def searchItem():
    """Returns a JSON data derived from making a database call based on user input

    Returns:
    json: Dynamically retrieved available items data

   """
    request_data = request.get_json()
    item = request_data['item']
    return jsonify({'data': searchItemHelper(item)})

@app.route('/itemLocator')
def locateItem():
    """Returns the item locator page of the web application along with the neccessary data

    Returns:
    file: The web page that will be returned
    pn: Dynamic product data
    loc: Dynamic location data
    fn: Static file name

   """
    hardcode_FileName = "test.png"

    return render_template('itemLocator.html', pn = global_Product, loc = global_Location, fn = hardcode_FileName)

@app.route('/pidlookup', methods=['POST'])
def productIDLookup():
    """Returns the product ID that is retrieved from the database

    Returns:
    pid: int value of the retrieved product ID

   """
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()

    output = request.get_json()
    result = json.loads(output) # this converts the json output to a python dictionary

    pid = result['selectRowID']
    product = result['selectRowProduct']
    global global_Product
    global_Product = product
    
    sql_LabelPoint = "SELECT logicalPoint FROM Label WHERE productID=" + pid
    cursor.execute(sql_LabelPoint)
    get_LogicalPoint = cursor.fetchone()
    global global_Location
    global_Location = str(get_LogicalPoint[0])

    return pid

# Add new Supermarket
@app.route('/insertSupermarket', methods = ["POST"])
def insertSupermarket():
    """Returns the manager page of the web application after a POST request to insert supermarket data

    Returns:
    file: The web page that will be returned

   """
    if (request.method == "POST"):
        supermarketName = request.form.get("new_supermerket")
        supermarketBranch = request.form.get("new_Branch")
        supermarketAddress = request.form.get("new_Address")
        insertSupermarketHelper(supermarketName, supermarketBranch, supermarketAddress)

    return render_template('Manager.html')

@app.route('/insert_Blueprint', methods = ["POST"])
def insertBlueprint():
    """Returns the product specification page of the web application after a POST request to insert blueprint data along with the file name

    Returns:
    file: The web page that will be returned
    BP_Filename: The file name of the uploaded blueprint

   """
    if (request.method == "POST"):
        supermarketName = request.form.get("sName")
        supermarketBranch = request.form.get("bName")
        
        input_File = request.files['fName']
        if input_File.filename == '':
            return redirect(url_for('/Manager'))
        else:
            supermarketBlueprint = secure_filename(input_File.filename)

        insertPhysicalFPHelper(supermarketName, supermarketBranch, str(supermarketBlueprint))
        return render_template('product_specifications.html', BP_Filename = str(supermarketBlueprint))
    
    
# Helper functions
def searchItemHelper(item):
    """Helper function that returns the data of the products based on user input

    Parameters:
    item (String): String value that is to be concatenated with the SQL statement

    Returns:
    data: The retrieved data from the database

   """
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sqlStatement = "SELECT * FROM Product WHERE name LIKE '%" + str(item) + "%'"
    cursor.execute(sqlStatement)
    data = cursor.fetchall()
    if not (cursor.rowcount == 0):
        return data
    else:
        return "Item not found!"

def getSupermarketHelper():
    """Helper function that returns the name of the products available in the supermarket

    Returns:
    record: The retrieved data from the database

   """
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
    """Helper function that returns the different branches of the supermarket

    Returns:
    record: The retrieved data from the database

   """
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sqlStatement = "SELECT DISTINCT branch FROM Supermarket"
    cursor.execute(sqlStatement)
    record = cursor.fetchall()
    if not (cursor.rowcount == 0):
        return record
    else:
        return "Cannot retrieve supermarket data, please try again!"

# Add new Supermarket Helper
def insertSupermarketHelper(supermarketName, supermarketBranch, supermarketAddress):
    """Helper function inserts the data of the supermarket into the database

    Parameters:
    supermarketName (String): String value that is to be concatenated with the SQL statement for insertion
    supermarketBranch (String): String value that is to be concatenated with the SQL statement for insertion
    supermarketAddress (String): String value that is to be concatenated with the SQL statement for insertion

   """
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sqlStatementSupermarket = "INSERT INTO Supermarket (name,branch,address) VALUES('"+ supermarketName +"', '"+ supermarketBranch +"', '"+ supermarketAddress +"')"
    cursor.execute(sqlStatementSupermarket)
    connection.commit()
    connection.close()

# Insert to PhysicalFP (Manager 1st page)
def insertPhysicalFPHelper(supermarket, branch, blueprint):
    """Helper function inserts the data of the product into the database

    Parameters:
    supermarket (String): String value that is to be concatenated with the SQL statement for insertion
    branch (String): String value that is to be concatenated with the SQL statement for insertion
    blueprint (String): String value that is to be concatenated with the SQL statement for insertion

   """
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

# Insert New Label
def insertLabel(PhyID, ProdID, location):
    """Helper function inserts the label into the database

    Parameters:
    PhyID (String): String value that is to be concatenated with the SQL statement for insertion
    ProdID (String): String value that is to be concatenated with the SQL statement for insertion
    location (String): String value that is to be concatenated with the SQL statement for insertion

   """
    connection = sqlite3.connect('../database/database.db')
    cursor = connection.cursor()
    sqlStatementLabel = "INSERT INTO Label (physicalID, productID, logicalPoint) VALUES ("+ PhyID +", "+ ProdID +", '"+ location +"')"
    cursor.execute(sqlStatementLabel)
    connection.commit()
    connection.close()

if __name__ == '__main__':
    # Run the Flask server
    print("\nFlask server started and listening on port 5000...\n")
    app.run(debug=True, host='0.0.0.0')
    
    