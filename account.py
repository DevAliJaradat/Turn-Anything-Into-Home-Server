import os
from argon2 import PasswordHasher, exceptions
server_conf =[line.strip().split('=') for line in open('server_conf.txt','r').readlines() if line[0]!='#' and line!='']
server_conf_dict = {e[0]:e[1] for e in server_conf}
USERS_DIR = server_conf_dict['USERS_DIR']
USERS_STORAGE_DIR = server_conf_dict['STORAGE_DIR']

if not os.path.exists(USERS_STORAGE_DIR):
    os.mkdir(USERS_STORAGE_DIR)
else:
    pass


# checks whether that directory exists or not
def check_accounts_dir_exists():
    if os.path.exists(USERS_DIR):
        return True
    else:
        os.mkdir(USERS_DIR)
    

# checks if the username is already taken or not
def valid_user(user):
    if f'{user}.txt' not in os.listdir(USERS_DIR):
        return True
    else:
        return False
    
def make_user(username:str,passwd:str):
    open(f'{USERS_DIR}/{username}.txt','w').write(f'{username}\n{hash_password(passwd)}')
    os.mkdir(f'{USERS_STORAGE_DIR}/{username}')
# encrypting passwords when saving them 
def hash_password(passwd: str)->str:
    return PasswordHasher().hash(passwd)

# to get data saved in user's file saved on the storage
def read_user_file(username:str)->list:
    return [line.strip() for line in open(f'./{USERS_DIR}/{username}.txt','r').readlines()]

#password checker
def check_password(username: str, passwd: str) -> bool:
    ph = PasswordHasher()
    res = read_user_file(username)[1]
    try:
        ph.verify(res, passwd)
        return True
    except exceptions.VerifyMismatchError:
        return False
    except Exception:
        return False


#sign up full function
def signup(user:str,passwd:str)->bool:
    try:
        
        if check_accounts_dir_exists() and valid_user(user):
            make_user(user,passwd)
            return True
        
    except Exception as e:
        return f'{e}'
    
def login(username: str, passwd: str) -> bool:
    if check_accounts_dir_exists() and not valid_user(username):
        return check_password(username, passwd)
    else:
        return False

