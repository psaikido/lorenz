#! /usr/bin/python

import re

chiOne = 41
chiTwo = 31

baudot = {
    " " : "00100",
    "," : "01000",
    "." : "00010",
    "?" : "00000",
    "!" : "11111",
    "'" : "11011",
    "A" : "00011",
    "B" : "11001",
    "C" : "01110",
    "D" : "01001",
    "E" : "00001",
    "F" : "01101",
    "G" : "11010",
    "H" : "10100",
    "I" : "00110",
    "J" : "01011",
    "K" : "01111",
    "L" : "10010",
    "M" : "11100",
    "N" : "01100",
    "O" : "11000",
    "P" : "10110",
    "Q" : "10111",
    "R" : "01010",
    "S" : "00101",
    "T" : "10000",
    "U" : "00111",
    "V" : "11110",
    "W" : "10011",
    "X" : "11101",
    "Y" : "10101",
    "Z" : "10001",
}

alphabet = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')

def code(plainText, settings):
    plainBytes = plainToBytes(plainText)
    keyBytes = plainToBytes(makeKeyStream(settings, len(plainText)))
    cipherBytes = bitwiseEncode(plainBytes, keyBytes)
    cipherText = bytesToPlain(cipherBytes)

    return cipherText


def xorBits(i, j):
    if i == j:
        return 0
    else:
        return 1

def xorBytes(a, b):
    tmpStr = ''

    for x in range(len(a)):
        tmpStr += str(xorBits(a[x], b[x]))

    return tmpStr

def bitwiseEncode(plainBytes, keyBytes):
    retA = []

    for x in range(len(plainBytes)):
        retA.append(xorBytes(plainBytes[x], keyBytes[x]))
        
    return retA

def makeChiArray(upperLimit, startingPos):
    chiAr = []
    y = startingPos

    for x in range(upperLimit):
        chiAr.append([
            alphabet[y],
            baudot[alphabet[y]]
            ])

        if y >= 25:
            y = 0
        else:
            y += 1

    return chiAr

def makeKeyStream(settings, keyLength):
    retStr = ""
    y = z = 0

    chiOneAr = makeChiArray(chiOne, settings[0])
    chiTwoAr = makeChiArray(chiTwo, settings[1])

    for x in range(keyLength):
        if y >= chiOne:
            y = 0
        if z >= chiTwo:
            z = 0
        chiOneByte = chiOneAr[y][1]
        chiTwoByte = chiTwoAr[z][1]
        xorProduct = xorBytes(list(chiOneByte), list(chiTwoByte))
        resultantLtr = list(baudot.keys())[list(baudot.values()).index(xorProduct)]
        retStr += resultantLtr
        
        y += 1
        z += 1

    return retStr

def bytesToPlain(cipherBytes):
    retStr = ''

    for fiveb in cipherBytes:
        retStr += list(baudot.keys())[list(baudot.values()).index(fiveb)]

    return retStr

def plainToBytes(plain):
    bits = []

    for c in list(plain):
        bits.append(baudot[c.upper()])

    return bits

"""
inpNo1 = int(input("no1? "))
inpNo2 = int(input("no2? "))
print("Lorenz can handle a-zA-Z letters and these characters ,.?!'")
msg = input("msg? ")
res = code(msg, [inpNo1, inpNo2])
print('Lorenz: ', res)
"""
