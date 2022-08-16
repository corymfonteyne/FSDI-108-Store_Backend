from unicodedata import category
from flask import Flask
import json
from data import me, catalog

app = Flask(__name__)



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

@app.get("/api/test")
def test_api(): 
    return json.dumps("OK")

# get api/about return the me dictionary as json
@app.get("/api/about")
def about_api(): 
    return json.dumps(me)


@app.get("/api/catalog")
def get_catalog():
    return json.dumps(catalog)
    # return the list of products

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


        
    
#  app.run(debug=True)