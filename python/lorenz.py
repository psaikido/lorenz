#! /usr/bin/python

from lorenz_cls import Lorenz


# User input
lorenz = Lorenz()
inpNo1 = int(input("no1? "))
inpNo2 = int(input("no2? "))
inpNo3 = int(input("no3? "))
print("Lorenz can handle a-zA-Z letters and these characters ,.?!'")
msg = input("msg? ")
res = lorenz.code(msg, [inpNo1, inpNo2, inpNo3])
#res = lorenz.code("abc", [0, 0, 0])
print('Lorenz: ', res)
