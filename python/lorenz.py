#! /usr/bin/python

import re

class Lorenz:
    chiWheels = [41, 31]

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

    def __init__(self):
        pass

    def code(self, plainText, settings):
        for c in plainText.upper():
            if c not in self.baudot.keys():
                return "Dissallowed character: " + c

        plainBytes = self.plainToBytes(plainText)
        keyBytes = self.plainToBytes(self.makeKeyStream(settings, len(plainText)))
        cipherBytes = self.bitwiseEncode(plainBytes, keyBytes)
        cipherText = self.bytesToPlain(cipherBytes)

        return cipherText


    def xorBits(self, i, j):
        if i == j:
            return 0
        else:
            return 1

    def xorBytes(self, a, b):
        tmpStr = ''

        for x in range(len(a)):
            tmpStr += str(self.xorBits(a[x], b[x]))

        return tmpStr

    def bitwiseEncode(self, plainBytes, keyBytes):
        retA = []

        for x in range(len(plainBytes)):
            retA.append(self.xorBytes(plainBytes[x], keyBytes[x]))
            
        return retA

    def makeChiArray(self, upperLimit, startingPos):
        chiAr = []
        y = startingPos

        for x in range(upperLimit):
            chiAr.append([
                self.alphabet[y],
                self.baudot[self.alphabet[y]]
                ])

            if y >= 25:
                y = 0
            else:
                y += 1

        return chiAr

    def makeKeyStream(self, settings, keyLength):
        retStr = ""
        y = z = 0

        chiOneAr = self.makeChiArray(self.chiWheels[0], settings[0])
        chiTwoAr = self.makeChiArray(self.chiWheels[1], settings[1])

        for x in range(keyLength):
            if y >= self.chiWheels[0]:
                y = 0
            if z >= self.chiWheels[1]:
                z = 0
            chiOneByte = chiOneAr[y][1]
            chiTwoByte = chiTwoAr[z][1]
            xorProduct = self.xorBytes(list(chiOneByte), list(chiTwoByte))
            resultantLtr = list(self.baudot.keys())[list(self.baudot.values()).index(xorProduct)]
            retStr += resultantLtr
            
            y += 1
            z += 1

        return retStr

    def bytesToPlain(self, cipherBytes):
        retStr = ''

        for fiveb in cipherBytes:
            retStr += list(self.baudot.keys())[list(self.baudot.values()).index(fiveb)]

        return retStr

    def plainToBytes(self, plain):
        bits = []

        for c in list(plain):
            bits.append(self.baudot[c.upper()])

        return bits


# User input
lorenz = Lorenz()
inpNo1 = int(input("no1? "))
inpNo2 = int(input("no2? "))
print("Lorenz can handle a-zA-Z letters and these characters ,.?!'")
msg = input("msg? ")
res = lorenz.code(msg, [inpNo1, inpNo2])
#res = lorenz.code("abc", [1, 1])
print('Lorenz: ', res)
