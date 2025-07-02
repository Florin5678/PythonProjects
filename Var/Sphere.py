pi = 3.1415926535897931
def main():
    r=input('Radius of the sphere: ')
    r2=""
    unitofmeasurement=""
    okinput=True
    for x in r:
        if x.isnumeric():
            if unitofmeasurement!="": okinput=False
            else: r2+=x
        elif x.isalpha():
            unitofmeasurement+=x
        else: okinput=False
    if okinput:
        V = 4.0/3.0 * pi * float(r2)**3
        print('The volume of the sphere is: ', V,end="")
        if unitofmeasurement!="": print(f" {unitofmeasurement}^3")
    else: print("Invalid input.")

if __name__ == "__main__":
    main()