
import pymongo
import certifi

con_str = "mongodb+srv://corymfonteyne:Goodluck123$@cluster0.o9huod1.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("arbormillcustoms")