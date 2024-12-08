key=4
item='d'
if key not in d:
    d[key]=[]
d[key].append(item)

# a long if statement
a=2>3
b=3>5
c=4>1
if a and b and c
    print('this is easy')

#instructor.get_certificate()
#student have attribute _id
#student._id # No
#student.get_id# YES

l=[3,5,7,8,12,4,6,1]
found=None
i=0
while i<len(l) and found is None:
    if l[i]%2 == 0:
        found = l[i]
    i+=1
if found is not None:
    print(found)


L=[('Gary',23),('christina',7),('Gillian',4),('Jacky',40)]
L.sort()
sorted(L) #return a new list

l2=sorted(L,key=compare_key) # use compare key to get the key
l3=sorted(L,key=lambda t:t[1])

def compare_key(t):
    #return the key of each tuple
    return t[1]


from typing import Any
class A:

    def __init__ (self, attr1, attr2):
        self.attr1=attr1
        self.attr2=attr2
        self.list1=[]
    def get_list(self):
        return self.list1[:] # return the copy of the list/dict

    def __eq__(self, other:Any)->bool:
        if not isinstance(other, A)
            return Fasle
        return self.attr1 == other.attr1 and self.attr2==other.attr2

class Stack:
    def __init__ (self):
        self.item =[]
    def push(self,item:Any)-> None:
        self.items.append(item)

    def pop(self) ->Any:
        self.items.pop()

    def is_empty(self):
        return len(self.items)==0
class Stack2: #Another stack implementation
    def __init__ (self):
        self.item =[]
    def push(self,item:Any)-> None:
        self.items.insert(0,item)

    def pop(self) ->Any:
        self.items.pop(0)

    def is_empty(self):
        return len(self.items)==0
