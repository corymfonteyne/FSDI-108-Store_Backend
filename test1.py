
from data import me


# get data from dictionary
print(me["first_name"])

# modift
me["color"] = "gray"

# add
me["age"] = 35

# rad non existing key
# print(["title"]) #crash your code
# check if key exists inside a dictionary
if "title" in me:
    print(me["title"])

# print the full address
# street num, city

address = me["address"]
print(address["street"] + " " + str(address["number"]) + "," + address["city"])