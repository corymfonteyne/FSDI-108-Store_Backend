from math import prod
from flask import Flask, request, abort
import json
import random 
from data import me, catalog
from flask_cors import CORS
from config import db
from bson import ObjectId

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

    prod = db.Products.find_one({"_id": ObjectId(id)})
    prod = fix_id(prod)
    return json.dumps(prod)


@app.get("/api/products/<category>")
def get_by_category(category):

    cursor = db.Products.find({})
    results = []
    for prod in cursor:
        prod = fix_id(prod)
        results.append(prod)
        

    return json.dumps(results)



@app.get("/api/count")
def catalog_count():
    cursor = db.Products.find({})
    products = []
    for prod in cursor:
        products.append(prod)

    count = len(products)
    return json.dumps(count)

@app.get("/api/catalog/total")
def catalog_total(): 
    total = 0
    cursor = db.Products.find({})
    for prod in cursor:
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

# create 2 endpoints to save/retreive CouponCodes
# post/api coupons to save couponCodes
# get/api coupons to retreive couponCodes

@app.get("/api/coupons")
def save_coupon():
    coupon = request.get_json()
    # validating
    if not "code" in coupon:
        abort(400, "code is required")

    if not "discount" in coupon:
        abort(400, "discount is required")

    db.CouponCodes.insert_one(coupon)
    coupon = fix_id(coupon)
    return json.dumps(coupon)


@app.get("/api/coupons")
def get_coupons():
    cursor = db.CouponCodes.find({})
    results = []
    for cp in cursor:
        cp = fix_id(cp)
        results.append(cp)

    return json.dumps(results)

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