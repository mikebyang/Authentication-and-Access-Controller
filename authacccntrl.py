import json
import sys

users = {}
user_grps = {}
obj_grps = {}
acc_per = {}

def req_length(minlength, maxlength):
    """
    Parameters-
    minlength: minimum number of CLI arguments that are required
    maxlengthL maximum number of CLI arguments that can be given

    Return-
    object determining if arguments passed satisfy conditions
    """
    return

def save(diction, key):
    """
    Parameters-
    diction: Dictionary to be saved
    key: JSON file key to be used

    Return-
    0 if success and 1 otherwise
    """ 
    data = {}
    data.setdefault(key,[])
    for dkey,value in diction.items():
        data[key].append({dkey:value})
    with open(key, 'w') as fw:
        json.dump(data,fw)
    print("Success: File has been saved.")
    return

def load(FileName):
    """
    Parameter-
    FileName: Name of the json file to be read (String)

    Return-
    Dictionary containing the lowest value pair stored in the json file
    """
    diction={}
    with open(FileName) as fw:
        data = json.load(fw)
        for JsonKey,JsonValue in data.items():
            for pair in JsonValue:
                for key,value in pair.items():
                    diction.update({key:value})
    return diction

def AddUser(User, Passw):
    """
    Parameters-
    User: New user to be added (String)
    Passw: Password for the new user (String)

    Return-
    Dictionary key-value pair using User as the key and Passw as the value
    """
    if users.get(User) != None:
        print("Failure: User already in the system!")
        sys.exit(1)
    else:
        users.update({User: Passw})
        print("Success: User has been added into the system!")
    return

def Authenticate(User, Passw):
    if users.get(User) == None:
        print("Failure: no such user!")
    elif users.get(User) != Passw:
        print("Failure: bad password!")
    else:
        print("Success!")
        print("Access granted!")
    return

def printgrp(Group):
    for name in Group:
        print(name)
    return

def AddUserToGroup(User, Group):
    if users.get(User) == None:
        print("Failure: user does not exist!")
    elif user_grps.get(Group) == None:
        user_grps.update({Group:[]})
        user_grps[Group].append(User)
        print("Success: user has been added to the group.")
        print(User)
    else:
        try:
            user_grps[Group].index(User)
            print("User already in group.")
        except:
            user_grps[Group].append(User)
            print("Success: user has been added to the group.")
            printgrp(user_grps.get(Group))
    return
    
def AddObjectToGroup(Obj, Group):
    if users.get(Obj) == None:
        print("Failure: user does not exist!")
    elif user_grps.get(Group) == None:
        user_grps.update({Group:[]})
        user_grps[Group].append(Obj)
        print("Success: object has been added to the group.")
        print(Obj)
    else:
        try:
            obj_grps[Group].index(Obj)
            print("Object already in group.")
        except:
            obj_grps[Group].append(Obj)
            print("Success: object has been added to the group.")
            printgrp(user_grps.get(Group))
    return

def AddAccess(Operation, UserGrp, ObjGrp):
    if ObjGrp == None:
        return
    else:
        return

def CanAccess(Operation, User, Obj):
    if Obj == None:
        return
    else:
        return