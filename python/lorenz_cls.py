#! /usr/bin/python

import re

class Lorenz:
    #chiWheelLengths = [41, 31]
    chiWheelLengths = [3, 4, 5]

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

    #debug = True
    debug = False

    def __init__(self):
        pass


    def code(self, plainText, settings):
        if self.debug:
            print(f"settings: {settings} :: msg: {plainText}")

        for c in plainText.upper():
            if c not in self.baudot.keys():
                return "Dissallowed character: " + c

        plainBytes = self.plainToBytes(plainText)
        if self.debug:
            print(f"plainBytes: {plainBytes}")

        keyBytes = self.makeKeyStream(settings, len(plainText))
        if self.debug:
            print(f"keyBytes:   {keyBytes}")

        cipherBytes = self.bitwiseEncode(plainBytes, keyBytes)
        if self.debug:
            print(f"cipherByts: {cipherBytes}")

        cipherText = self.bytesToPlain(cipherBytes)
        if self.debug:
            print(f"cipherText: {cipherText}")

        return cipherText


    def makeKeyStream(self, settings, keyLength):
        retStr = ""
        chiWheels = []
        firstTransform = []

        for x in range(len(self.chiWheelLengths)):
            wh = self.makeChiArray(self.chiWheelLengths[x], settings[x])
            chiWheels.append(wh)

        firstTransform = self.xorWheelPair(keyLength, chiWheels[0], chiWheels[1])
        if self.debug:
            print(f"firstTranm: {firstTransform}")

        secondTransform = self.xorWheelPair(keyLength, firstTransform, chiWheels[2])
        if self.debug:
            print(f"secondTrnm: {secondTransform}")
        
        return secondTransform


    def xorWheelPair(self, keyLength, wheelOne, wheelTwo):
        if self.debug:
            print(f"wheelOne:   {wheelOne}")
            print(f"wheelTwo:   {wheelTwo}")

        bytes = []
        y = z = 0

        for x in range(keyLength):
            if y >= len(wheelOne):
                y = 0
            if z >= len(wheelTwo):
                z = 0

            chiOneByte = wheelOne[y]
            chiTwoByte = wheelTwo[z]
            bytes.append(self.xorBytes(list(chiOneByte), list(chiTwoByte)))

            y += 1
            z += 1
        
        return bytes 



    def makeChiArray(self, upperLimit, startingPos):
        chiAr = []
        y = startingPos

        for x in range(upperLimit):
            chiAr.append(self.baudot[self.alphabet[y]])

            if y >= 25:
                y = 0
            else:
                y += 1

        return chiAr


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


"""
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
"""
