import os
import sys
from configparser import ConfigParser

configFile = os.path.join(os.getcwd(), sys.argv[1])
cf=ConfigParser(allow_no_value=True)
cf.read(configFile, encoding='utf-8')

for section in cf.sections():
    print("section : {}".format(section))
    for option in cf.options(section):
        value = cf.get('kysy','wombat_user')
        print("option : {}, value : {}".format(option, value))
