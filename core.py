import argparse as ap
import sys
import authacccntrl as aac

#load and save load only relevant files
#command line parsing
parser = ap.ArgumentParser(description="Simple authentication and access library")
#possible flags
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-addu","--adduser",help="Define a new user for the system along with the user’s password, both strings.",nargs=2)
group.add_argument("-auth","--authenticate",help="Validate a user’s password by passing the username and password, both strings.",nargs=2)
group.add_argument("-addug","--addusertogroup",help="Add a user to a user group. If the group name does not exist, it is created. If a user does not exist, the function should return an error.",nargs=2)
group.add_argument("-addog","--addobjecttogroup",help="Add an object to an object group. If the group name does not exist, it is created. The object can be any string.",nargs=2)
group.add_argument("-adda","--addaccess",help="Define an access right: a string that defines an access permission of a user group to an object group. The access permission can be an arbitrary string that makes sense to the service.",nargs='+',action=aac.req_length(2,3))
group.add_argument("-cana","--canaccess",help="Test whether a user can perform a specified operation on an object. Optionally, an object may be NULL, in which case CanAccess checks allows access if a user is part of a group for an operation on which no object group was defined.",nargs='+',action=aac.req_length(2,3))
args = parser.parse_args()
#load the correct files
try:
    if args.adduser or args.authenticate:
        aac.users = aac.load("users")
    elif args.addusertogroup or args.addobjecttogroup:
        aac.user_grps = aac.load("user_grps")
        aac.obj_grps = aac.load("obj_grps")
    elif args.addaccess or args.canaccess:
        aac.acc_per = aac.load("acc_per")
except FileNotFoundError as FNFE:
    print("No user file was found.")
except Exception as e:
    print("Unknown error has occured:")
    print(e)
#execution
if args.adduser:
    aac.AddUser(args.adduser[0], args.adduser[1])
elif args.authenticate:
    aac.Authenticate(args.authenticate[0],args.authenticate[1])
elif args.addusertogroup:
    aac.AddUserToGroup(args.addusertogroup[0],args.addusertogroup[1])
elif args.addobjecttogroup:
    aac.AddObjectToGroup(args.addobjecttogroup[0],args.addobjecttogroup[1])
elif args.addaccess:
    aac.AddAccess()
elif args.canaccess:
    aac.CanAccess()
#save to correct files and exit
if args.adduser or args.authenticate:
    aac.save(aac.users, "users")
elif args.addusertogroup or args.addobjecttogroup:
    aac.save(aac.user_grps, "user_grps")
    aac.save(aac.obj_grps,"obj_grps")
elif args.addaccess or args.canaccess:
    aac.save(aac.acc_per,"acc_per")
print("Shutting down.....")
sys.exit(0)
