# Open a file
myFile = open("myfile.txt","w") # w for writing

print("Name: ", myFile.name)
print("Is Closed: ", myFile.closed)
print("Opening Mode: ", myFile.mode)

# Write to file
myFile.write("Awebo")
myFile.write("\nAwebus")
myFile.close()

# Append to file
myFile = open("myfile.txt","a") # a for append
myFile.write("\nAwebersen")
myFile.close()

# Read from file
myFile = open("myfile.txt","r+") # a for append
print(myFile.read(100))
myFile.close()
