# class = the blueprint of an object. An object has properties and methods (functions) associated with it

# create class
class User :
    # Constructor
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age
    def greeting(self):
        return f"My name is {self.name} and I am {self.age}."
    def has_birthday(self):
        self.age += 1

# init user object
brad = User('Brad', 'brad@gmail.com', 37)

print(type(brad))
print(brad.name)

print(brad.greeting())
brad.has_birthday()
print(brad.greeting())

# Extend class
class Customer(User) :
    # Constructor
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age
        self.balance = 0
    def greeting(self):
        return f"My name is {self.name} and I am {self.age} and my balance is {self.balance}."
    def set_balance(self,balance):
        self.balance = balance

janet = Customer("Janet","janet@gmail.com",25)
janet.set_balance(500)
print(janet.greeting())
janet.has_birthday() # possible because Customer extends User
print(janet.greeting())