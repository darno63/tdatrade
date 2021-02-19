from configparser import ConfigParser


def get_tokens(tokens):
    config = ConfigParser()
    config.read('auth\\tokens.ini')
    tdakeys = config['TD AMERITRADE']
    if type(tokens) == str:
        return tdakeys[tokens]
    if type(tokens) == list:
        return_tokens = []
        for i in tokens:
            return_tokens.append(tdakeys[i])
        return return_tokens

def save_tokens(**kwargs):
    config = ConfigParser()
    config.read('auth\\tokens.ini')
    to_write = False
    if bool(kwargs):
        for key in kwargs:
            f_key = key.replace("_", " ")
            f_val = str(kwargs[key])
            config.set('TD AMERITRADE', f_key, f_val)
        with open('auth\\tokens.ini', 'w') as file:
            config.write(file)
    else:
        print("error: args are wrong")

# https://docs.python.org/3/library/configparser.html

