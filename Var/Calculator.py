acceptedsigns = [" ", "+", "-", "*", "/", "^", "%", "(", ")", "[", "]", "{", "}"]
def isvalidinput(n):
    openparantheses=" "
    for x in n:
        if not(x.isnumeric() or acceptedsigns.count(x)>0): return False
        match x:
            case "(":
                if openparantheses[-1]=="(": return False
                else: openparantheses+="("
            case ")":
                if openparantheses[-1]=="(": openparantheses=openparantheses[:-1]
                else: return False
            case "[":
                if openparantheses[-1]=="[" or openparantheses[-1]=="(": return False
                else: openparantheses+="["
            case "]":
                if openparantheses[-1]=="(": return False
                elif openparantheses[-1]=="[": openparantheses=openparantheses[:-1]
                else: return False
            case "{":
                if openparantheses[-1]=="{" or openparantheses[-1]=="[" or openparantheses[-1]=="(": return False
                else: openparantheses+="{"
            case "}":
                if openparantheses[-1]=="[" or openparantheses[-1]=="(": return False
                elif openparantheses[-1]=="{": openparantheses=openparantheses[:-1]
                else: return False
    return True
def sep(n, operator):
    if isinstance(n,str):
        if n.find(operator)>-1:
            n=n.split(operator)
            templist=[n[0]]
            for x in range(1,len(n)):
                templist.append(operator)
                templist.append(n[x])
            n=templist
    return n
def sep2(n,op1,op2):
    n=sep(n,op1)
    if isinstance(n,list):
        templist=[]
        for x in n:
            x=sep(x,op2)
            if isinstance(x,list): templist.extend(x)
            else: templist.append(x)
        return templist
    return sep(n,op2)
def removenull(n):
    nullcount = n.count("")
    while (nullcount>0):
        n.remove("")
        nullcount-=1
    return n
def exp(n):
    n=sep(n,"^")
    if isinstance(n,list):
        base=float(n[0])
        exp=1
        for x in range(2,len(n)):
            if n[x-1]=="^": exp*=float(n[x])
        return base**exp
    return n
def percent(n):
    while isinstance(n,str) and n.find("%") > 0:
        templist=n.split("%",1)
        n=str(float(templist[0])/ 100)+templist[1]
    return n
def muldiv(n):
    n=sep2(n,"*","/")
    if isinstance(n,list):
        n=removenull(n)
        result=1
        for x in range(0,len(n)):
            n[x]=percent(n[x])
            elem=exp(n[x])
            if elem!="*" and elem!="/":
                if x==0 or n[x-1]=="*": result*=float(elem)
                elif n[x-1]=="/": result/=float(elem)
        return result
    n=percent(n)
    return exp(n)
def addsub(n):
    n=sep2(n,"+","-")
    if (isinstance(n,list)):
        n=removenull(n)
        x=0
        while x<len(n)-1:
            if x==0 and n[x]=="-":
                n[x] += n[x + 1]
                n.pop(x+1)
            elif x>0 and n[x]=="-" and (n[x-1][len(n[x-1])-1]=="*" or n[x-1][len(n[x-1])-1]=="/"):
                n[x-1]+=n[x]+n[x+1]
                n.pop(x)
                n.pop(x)
            else: x+=1

        result=0
        for x in range(0,len(n)):
            elem = muldiv(n[x])
            if (x==0 or n[x-1]=="+") and n[x]!="-" and n[x]!="+": result+=float(elem)
            elif n[x-1]=="-": result-=float(elem)
        return result
    return muldiv(n)
def para(n):
    n=sep2(n,"(",")")
    if isinstance(n,list):
        n=removenull(n)
        #print(n)
        result=""
        for x in range(0,len(n)):
            if n[x]=="(":
                if x>0:
                    tempstr=n[x-1]
                    if n[x-1]==")":
                        result+="*"
                    elif acceptedsigns.count(tempstr[len(tempstr)-1]):
                        result+=tempstr
                    else:
                        result+=tempstr+"*"
                result+=str(addsub(n[x+1]))
            elif x<len(n)-1 and n[x]==")" and n[x+1][0].isnumeric(): result+="*"
            elif x==len(n)-1 and n[x]!=")": result+=n[x]
        if result.find("[")>-1:
            result=result.replace("[","(")
            result=result.replace("]",")")
            if result.find("{")>-1:
                result=result.replace("{","[")
                result=result.replace("}","]")
            result=para(result)
        return addsub(result)
    return addsub(n)
def calc(n):
    n=para(n)
    if n*10%10==0: n=int(n)
    print(n)
def main():
    while True:
        n=input("Submit calculation.\nAccepted operations: + - * / ^ % () [] {}\n")
        if isvalidinput(n): calc(n)
        else: input("Invalid input.")

if __name__ == "__main__":
    main()