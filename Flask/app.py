# Imports
import io
import csv
import random
import datetime
import os
from urllib import response
from flask import Flask, render_template, json, Response, redirect, redirect, jsonify

# gRPC Imports
import grpc
import item_locator_pb2
import item_locator_pb2_grpc
from concurrent import futures
import logging

app = Flask(__name__)

@app.route('/')
def index():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = item_locator_pb2_grpc.ItemLocatorStub(channel)
        response = stub.SearchItem(item_locator_pb2.Request(name='test'))
        print("\n[!] gRPC Response: ", str(response.res), "\n")
    
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask server
    print("Flask server started and listening on port 5000...\n")
    app.run(debug=True)
    
    