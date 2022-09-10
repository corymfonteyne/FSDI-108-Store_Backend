from math import prod
from flask import Flask, request, abort
import json
import random 
from data import me, catalog
from flask_cors import CORS
from config import db

app = Flask(__name__)
CORS(app) # diable CORS, anyone can access this API


@app.get("/")
def home():
    return "Hello from flask"

@app.get("/test")
def test(): 
    return "This is just another endpoint"




#get /about returns your name

@app.get("/about")
def about():
    return "Cory Fonteyne"

###################
# APIProducts #
###################

def fix_id(obj):
    obj["_id"] = str(obj["_id"])
    return obj

@app.get("/api/test")
def test_api(): 
    return json.dumps("OK")

# get api/about return the me dictionary as json
@app.get("/api/about")
def about_api(): 
    return json.dumps(me)


@app.get("/api/catalog")
def get_catalog():
    cursor = db.Products.find({}) # read all products
    results = []
    for prod in cursor:
        prod = fix_id(prod)
        results.append(prod)

    return json.dumps(results)
    # return the list of products

@app.post("/api/catalog")
def save_product():
    product = request.get_json()
    # validating
    if not "title" in product:
        return abort(400,"ERROR: Title is required")

    # title must have a tleast five characters
    if len(product["title"]) < 5:
        return abort(400,"ERROR: Title must be at least 5 characters")

    # must have a price
    if not "price" in product:
        return abort(400,"ERROR: Price is required")
    # price must be greater than 1
    if product["price"] < 1:
        return abort(400,"ERROR: Price must be greater than 1")

    db.Products.insert_one(product)
    print(product) #it should have an _id assigned by the DB

    return json.dumps(product)

@app.get('/api/product/<id>')
def get_product_by_id(id):
    for prod in catalog:
        if prod["_id"] == id:
            return json.dumps(prod)

    return json.dumps("Error: Id not valid")

@app.get("/api/products/<category>")
def get_product_by_category(category):
    results = []
    for prod in catalog:
        if prod["category"] == category:
            results.append(prod)

    return json.dumps(results)



@app.get("/api/count")
def catalog_count(): 
    count = len(catalog)
    return json.dumps(count)

@app.get("/api/catalog/total")
def catalog_total(): 
    total = 0
    for prod in catalog:
        total += prod["price"]

    return json.dumps(total)

# get api/catalog/cheapest
@app.get("/api/catalog/cheapest")
def catalog_cheapest(): 
    cheapest = catalog[0]
    for prod in catalog:
         if prod["price"] < cheapest["price"]:
            cheapest = prod

    return  json.dumps(cheapest)

# play rock, paper, scissors
# /api/game/paper
# return should be a dictionary (as json)
# {
#   "you": paper,
#   "pc": rock,
#   "winner": you
# }

# step 1: create endpoint return {"you": rock }

@app.get("/api/game/<pick>")
def game(pick):

 # random pick
    num = random.randint(0,2)
    pc = ""
    if num == 0:
        pc = "paper"
    elif num == 1:
        pc = "rock"
    else:
        pc = "scissors"

    winner = ""
    if pick == "paper":
        if pc == "rock":
            winner = "you"
        elif pc == "scissors":
            winner = "pc" 
        else:
            winner = "draw"

    elif pick == "rock":
        if pc == "rock":
            winner = "draw"
        elif pc == "scissors":
            winner = "you" 
        else:
            winner = "pc"

    elif pick == "scissors":
        if pc == "rock":
            winner = "pc"
        elif pc == "scissors":
            winner = "draw" 
        else:
            winner = "you"

    results = {
        "you": pick,
        "pc": pc,
        "winner": winner
    }


    return json.dumps(results)

# step 2: generate a random number between 0 and 2
# change the number to be rock, paper or scissors
# return 
# {
#   "you": paper,
#   "pc": rock,
# }

# step 3
# finish the logic to pick the winner




        
    
#  app.run(debug=True)