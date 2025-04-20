"""
# conditionals
y = 10

def compare(x,y):
    if x > y : print (f"{x} is greater than {y}.")
    elif x < y : print(f"{x} is less than than {y}.")
    else : print(f"{x} is equal to {y}.")

for x in (5,10,15) : compare(x,y)

if x > 2 and x <= 15 : print(f"{x} is greater than 2 and less than or equal to 15")
if not(x == y) : print(f"{x} is not equal to {y}.")
"""
"""
# membership operators
numbers = [1,2,3,4,5]
x = y = 3
print(x in numbers)
print(x not in numbers)
print(x is y)
print(x is not y)
"""

# for loops
"""
people = ['John','Paul','Janet','Sara','Susan']
for person in people :
    if (person=='Paul') : continue
    if (person=='Sara') : break
    print(person)
for i in range(len(people)) : print(people[i])
for i in range(0,6) : print(i)
"""

# while loops
"""
count = 0
while count <= 10 :
    print(f"Count : {count}")
    count += 1
"""