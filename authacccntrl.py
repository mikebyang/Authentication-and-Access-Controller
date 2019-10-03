import json
import sys

users = {}
user_grps = {}
obj_grps = {}
acc_per = {}

def save(diction, key):
    """
    Save the dictionary to file with the name stored in key

    Parameters-
    diction: Dictionary to be saved
    key: JSON file key to be used
    """ 
    data = {}
    data.setdefault(key,[])
    for dkey,value in diction.items():
        data[key].append({dkey:value})
    with open(key, 'w') as fw:
        json.dump(data,fw)
    print("Success: %s file has been saved."%(key))
    return

def load(FileName):
    """
    Load the dictionary from file

    Parameter-
    FileName: Name of the json file to be read (String)

    Return-
    Dictionary containing the dictionary stored in the json file
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
    Adds user-password pair into the system

    Parameters-
    User: New user to be added (string)
    Passw: Password for the new user (string)
    """
    if users.get(User) != None:
        print("Failure: User already in the system!")
        sys.exit(1)
    else:
        users.setdefault(User, Passw)
        print("Success: User has been added into the system!")
    return

def Authenticate(User, Passw):
    """
    Checks if user-password pair is in the system

    Parameters-
    User- User in the system (string)
    Passw- Password for the user (string)
    """
    if users.get(User) == None:
        print("Failure: no such user!")
        sys.exit(1)
    elif users.get(User) != Passw:
        print("Failure: bad password!")
        sys.exit(1)
    else:
        print("Success!")
        print("Access granted!")
    return

def printgrp(Group):
    """
    Prints the users in the group

    Parameter-
    Group: List of users
    """
    for name in Group:
        print(name)
    return

def AddUserToGroup(User, Group):
    """
    Adds existing user to existing group or new group
    
    Parameters-
    User: Existing user in the system (string)
    Group: Existing group or name of group to be created (string)
    """
    if users.get(User) == None:
        #user exists in the system
        print("Failure: user does not exist!")
        sys.exit(1)
    elif user_grps.get(Group) == None:
        user_grps.setdefault(Group,[])
        user_grps[Group].append(User)
        print("Success: user has been added to the group.")
        print(User)
    else:
        try:
            #user is in the group
            user_grps[Group].index(User)
            print("User already in group.")
            sys.exit(1)
        except:
            user_grps[Group].append(User)
            print("Success: user has been added to the group.")
            printgrp(user_grps.get(Group))
    return
    
def AddObjectToGroup(Obj, Group):
    """
    Adds object to existing group or new group

    Parameters-
    Obj: Object name (string)
    Group: Existing group or name of group to be created (string)
    """
    if obj_grps.get(Group) == None:
        #object group does not exist
        obj_grps.setdefault(Group,[])
        obj_grps[Group].append(Obj)
        print("Success: object has been added to the group.")
        print(Obj)
    else:
        if Obj in obj_grps[Group]:
            #object exists in the group
            print("Object already in group.")
            sys.exit(1)
        else:
            #object does not in the group
            obj_grps[Group].append(Obj)
            print("Success: object has been added to the group.")
            printgrp(obj_grps.get(Group))
    return

def argscheck(arglist):
    """
    Checks if number of parameters passed is between 2 and 3 inclusive

    Parameters-
    arglist: list of parameters

    Return-
    Boolean value determining if the correct number of parameters was passed
    """
    if len(arglist)<2 or len(arglist)>3:
        return False
    else:
        return True

def AddAccess(Operation, UserGrp, ObjGrp):
    """
    Gives user group access to an operation
    
    Parameters-
    Operation: operation that acces is being granted for (string)
    UserGrp: user group that is gaining access (string)
    ObjGrp: object group in which the user group is being allowed to use the operation on (string)
    ObjGrp(None): case in which user group has universal access to operation
    """
    if UserGrp not in user_grps:
        #user group does not exist
        print("Error: user group does not exist.")
        sys.exit(1)
    elif ObjGrp == None:
        #no object group is provided
        if acc_per.get(Operation) == None:
            #operation does not exist in access dictionary
            acc_per.setdefault(Operation, {UserGrp:None})
        else:
            acc_per[Operation].update({UserGrp:None})
        print("%s operation access has been granted for user group, %s."%(Operation,UserGrp))
    elif ObjGrp not in obj_grps:
        #object group does not exist
        print("Error: object group does not exist.")
        sys.exit(1)
    else:
        if acc_per.get(Operation) == None:
            #operation does not exist in access dictionary
            acc_per.setdefault(Operation, {})
            acc_per[Operation].setdefault(UserGrp,[])
            acc_per[Operation][UserGrp].append(ObjGrp)
        else:
            if UserGrp not in acc_per[Operation]:
                #if user has not been given permission to this operation before
                acc_per[Operation].setdefault(UserGrp,[])
                acc_per[Operation][UserGrp].append(ObjGrp)
            elif ObjGrp in acc_per[Operation][UserGrp]:
                print("%s already has permission for performing %s on object group, %s."%(UserGrp,Operation,ObjGrp))
                sys.exit(1)
            else:
                acc_per[Operation][UserGrp].append(ObjGrp)
        print("%s operation access for object group, %s, has been granted to user group, %s."%(Operation,ObjGrp,UserGrp))
    return

def checkUser(operation, user):
    """
    Checks to see if user has access to the operation.

    Parameters-
    operation: operation in question
    user: user that may or may not have access to the operation

    Return-
    boolean which describes if user has access to operation and group with user in it
    """
    for usegroup in acc_per[operation]:
        if user in user_grps[usegroup]:
            return True,usegroup
    return False,None

def CanAccess(Operation, User, Obj):
    """
    Checks operation access permissions for a user

    Parameters-
    Operation: operation name (string)
    User: name of user whose access permissions is being checked (string)
    Obj: obj name (string)
    Obj(None): user only has access if addaccess was used without an ObjGrp field
    """
    #find if operation permission has been granted to any user group
    if Operation not in acc_per:
        print("Error: permission for operation has not been granted to any user groups.")
        sys.exit(1)
    check, group = checkUser(Operation,User)
    if Obj == None:
        #object field is not provided
        if check:
            #user is in a group with access to operation
            if acc_per[Operation][group] == None:
                print("%s is in a group with universal access to operation, %s."%(User,Operation))
            else:
                print("Error: user is in a group that does not have universal access to operation, %s."%(Operation))
                sys.exit(1)
        else:
            print("Error: user is not in a group with access to operation, %s."%(Operation))
            sys.exit(1)
    else:
        if check:
            #user is in a group with access to operation
            if acc_per[Operation][group] == None:
                print("%s has permission to perform operation, %s, on object, %s."%(User,Operation,Obj))
            elif Obj in acc_per[Operation][group]:
                print("%s has permission to perform operation, %s, on object, %s."%(User,Operation,Obj))
        else:
            print("Error: user is not in a group with access to operation, %s."%(Operation))
            sys.exit(1)
    return