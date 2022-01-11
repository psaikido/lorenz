#! /usr/bin/python

from lorenz_cls import Lorenz


# User input
lorenz = Lorenz()

print("Lorenz wheel settings as 3, comma separated numbers: ")
settingsInput = input("settings: ").split(',')
settings = [int(x) for x in settingsInput]

print("Lorenz can handle a-zA-Z letters and these characters ,.?!'")
msg = input("msg? ")
res = lorenz.code(msg, settings)
print('Lorenz: ', res)
