import argparse as ap
import sys
import authacccntrl as aac

#command line parsing
parser = ap.ArgumentParser(prog="Authentication and Access",description="Simple authentication and access library")
#possible flags
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-addu","--adduser",help="Define a new user for the system along with the user’s password, both strings. (User, Password)",nargs=2)
group.add_argument("-auth","--authenticate",help="Validate a user’s password by passing the username and password, both strings. (User, Password)",nargs=2)
group.add_argument("-addug","--addusertogroup",help="Add a user to a user group. If the group name does not exist, it is created. If a user does not exist, the function should return an error. (User, Group)",nargs=2)
group.add_argument("-addog","--addobjecttogroup",help="Add an object to an object group. If the group name does not exist, it is created. The object can be any string. (Object, Group)",nargs=2)
group.add_argument("-adda","--addaccess",help="Define an access right: a string that defines an access permission of a user group to an object group. The access permission can be an arbitrary string that makes sense to the service. (Operation, User Group, Object Group)",nargs='*')
group.add_argument("-cana","--canaccess",help="Test whether a user can perform a specified operation on an object. Optionally, an object may be NULL, in which case CanAccess checks allows access if a user is part of a group for an operation on which no object group was defined. (Operation, User, Object)",nargs='*')
args = parser.parse_args()
#load the correct files
try:
    if args.adduser or args.authenticate:
        aac.users = aac.load("users")
    elif args.addusertogroup:
        aac.users = aac.load("users")
        aac.user_grps = aac.load("user_grps")
    elif args.addobjecttogroup:
        aac.obj_grps = aac.load("obj_grps")
    elif args.addaccess or args.canaccess:
        if args.addaccess != None:
            if not aac.argscheck(args.addaccess):
                parser.print_help()
                sys.exit(1)
        elif args.canaccess != None:
            if not aac.argscheck(args.canaccess):
                parser.print_help()
                sys.exit(1)
        aac.user_grps = aac.load("user_grps")
        aac.obj_grps = aac.load("obj_grps")
        aac.acc_per = aac.load("acc_per")
except FileNotFoundError as FNFE:
    print("No user file was found.")
    print(FNFE)
except Exception as e:
    print("Unknown error has occured:")
    print(e)
#function execution
if args.adduser:
    aac.AddUser(args.adduser[0], args.adduser[1])
elif args.authenticate:
    aac.Authenticate(args.authenticate[0],args.authenticate[1])
elif args.addusertogroup:
    aac.AddUserToGroup(args.addusertogroup[0],args.addusertogroup[1])
elif args.addobjecttogroup:
    aac.AddObjectToGroup(args.addobjecttogroup[0],args.addobjecttogroup[1])
elif args.addaccess:
    if len(args.addaccess) == 3:
        aac.AddAccess(args.addaccess[0],args.addaccess[1],args.addaccess[2])
    else:
        aac.AddAccess(args.addaccess[0],args.addaccess[1],None)
elif args.canaccess:
    if len(args.canaccess) == 3:
        aac.CanAccess(args.canaccess[0],args.canaccess[1],args.canaccess[2])
    else:
        aac.CanAccess(args.canaccess[0],args.canaccess[1],None)
#save to correct files and exit
try:
    if args.adduser or args.authenticate:
        aac.save(aac.users, "users")
    elif args.addusertogroup:
        aac.save(aac.user_grps, "user_grps")
    elif args.addobjecttogroup:
        aac.save(aac.obj_grps,"obj_grps")
    elif args.addaccess or args.canaccess:
        aac.save(aac.acc_per,"acc_per")
except Exception as e:
    print(e)
print("Shutting down.....")
sys.exit(0)
