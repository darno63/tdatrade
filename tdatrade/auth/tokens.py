from configparser import ConfigParser
import os

FILE_LOCATION = os.getcwd() + '\\tokens.ini'

def get_tokens(tokens):
    if os.path.exists(FILE_LOCATION) == False:
        create_tokens_ini()
    
    if os.path.exists(FILE_LOCATION) == True:
        config = ConfigParser()
        config.read(FILE_LOCATION)
        tdakeys = config['TD AMERITRADE']
        if type(tokens) == str:
            return tdakeys[tokens]
        if type(tokens) == list:
            return_tokens = []
            for i in tokens:
                return_tokens.append(tdakeys[i])
            return return_tokens

def save_tokens(**kwargs):

    if os.path.exists(FILE_LOCATION) == False:
        create_tokens_ini()

    if os.path.exists(FILE_LOCATION) == True:
        config = ConfigParser()
        config.read(FILE_LOCATION)
        to_write = False
        if bool(kwargs):
            for key in kwargs:
                f_key = key.replace("_", " ")
                f_val = str(kwargs[key])
                config.set('TD AMERITRADE', f_key, f_val)
            with open(FILE_LOCATION, 'w') as file:
                config.write(file)
        else:
            print("error: args are wrong")

def create_tokens_ini():
    print("\nNo tokens.ini file found")
    client_id = input("To create new ini file please input Consumer Key:\n")
    account_number = input("input Account number:\n")
    config = ConfigParser()
    config.read(FILE_LOCATION)
    config['TD AMERITRADE'] = {'client id': client_id + r'@AMER.OAUTHAP', 'account number': account_number}
    with open(FILE_LOCATION, 'w') as file:
        config.write(file)

# https://docs.python.org/3/library/configparser.html

