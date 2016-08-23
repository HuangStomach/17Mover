import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("../config/site.conf") 

def get (path):
    path = path.split(".", 2)
    return cf.get(path[0], path[1])
