import sys
import traceback
import os
from pwd import getpwnam  
from pwd import getpwuid 
import time
import grp

def tracefunc(frame, event, arg, indent=[0]):
	timestr = ""
	if frame.f_code.co_name != "_remove":
		timestr = time.ctime(time.time())

	if event == "call":
		indent[0] += 2
		print timestr, "-" * indent[0] + "> call function", frame.f_code.co_name
	elif event == "return":
		print timestr, "<" + "-" * indent[0], "exit function", frame.f_code.co_name
		indent[0] -= 2
	return tracefunc

def acl2mode(acl):
    modeDict = {
        "r" : os.R_OK,
        "w" : os.W_OK,
        "x" : os.X_OK,
    }
    return modeDict[acl]

def getUserGids(name):
    return [g.gr_gid for g in grp.getgrall() if name in g.gr_mem]
    
def getUserInfo(user):
    try:
        return getpwuid(int(user))
    except:
        return getpwnam(user)

def _accessFile(path, user, acl):
    mode = acl2mode(acl)
    userInfo = getUserInfo(user)
    gids = getUserGids(userInfo.pw_name)
    os.setgid(userInfo.pw_gid)
    os.setgroups(gids)
    os.setuid(userInfo.pw_uid)
    ret = os.access(path, mode)
    if ret == False:
        return 1
    else:
        return 0

#python accessFile.py $path $user $acl
def main():
    path = sys.argv[1]
    user = sys.argv[2]
    acl = sys.argv[3]
    if _accessFile(path, user, acl) == 0:
        sys.exit(0)
    else:
        sys.exit(-1)

if __name__ == "__main__":
    sys.settrace(tracefunc)
    main()
