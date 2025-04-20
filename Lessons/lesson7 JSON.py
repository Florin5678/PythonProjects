# JSON is commonly used with data APIS. Here is how we can parse JSON into a Python dictionary

import json

# JSON to Dictionary
userJSON = '{"first_name" : "John", "last_name" : "Doe", "age" : 30}'
user = json.loads(userJSON)

print(user)
print(user["first_name"])

# Dictionary to JSON
car = {"make" : "Ford", "model" : "Mustang", "year" : 1970}
carJSON = json.dumps(car)
print(carJSON)