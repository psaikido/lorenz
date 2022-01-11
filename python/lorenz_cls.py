#! /usr/bin/python

import re

class Lorenz:
    chiWheelLengths = [41, 31, 29]

    baudot = (
        {"char" : "A", "code" : "00011"},
        {"char" : "B", "code" : "11001"},
        {"char" : "C", "code" : "01110"},
        {"char" : "D", "code" : "01001"},
        {"char" : "E", "code" : "00001"},
        {"char" : "F", "code" : "01101"},
        {"char" : "G", "code" : "11010"},
        {"char" : "H", "code" : "10100"},
        {"char" : "I", "code" : "00110"},
        {"char" : "J", "code" : "01011"},
        {"char" : "K", "code" : "01111"},
        {"char" : "L", "code" : "10010"},
        {"char" : "M", "code" : "11100"},
        {"char" : "N", "code" : "01100"},
        {"char" : "O", "code" : "11000"},
        {"char" : "P", "code" : "10110"},
        {"char" : "Q", "code" : "10111"},
        {"char" : "R", "code" : "01010"},
        {"char" : "S", "code" : "00101"},
        {"char" : "T", "code" : "10000"},
        {"char" : "U", "code" : "00111"},
        {"char" : "V", "code" : "11110"},
        {"char" : "W", "code" : "10011"},
        {"char" : "X", "code" : "11101"},
        {"char" : "Y", "code" : "10101"},
        {"char" : "Z", "code" : "10001"},
        {"char" : " ", "code" : "00100"},
        {"char" : ",", "code" : "01000"},
        {"char" : ".", "code" : "00010"},
        {"char" : "?", "code" : "00000"},
        {"char" : "!", "code" : "11111"},
        {"char" : "'", "code" : "11011"}
    )

    #debug = True
    debug = False

    def __init__(self):
        pass


    def code(self, plainText, settings):
        if self.debug:
            print(f"settings: {settings} :: msg: {plainText}")

        for c in plainText.upper():
            found = False

            for i in range(len(self.baudot)):
                if self.baudot[i]["char"] == c:
                    found = True
                    break

            if found != True:
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
            chiAr.append(self.baudot[y]["code"])

            if y >= 25:
                y = 0
            else:
                y += 1

        return chiAr


    def bytesToPlain(self, bytes):
        retStr = ''

        for byte in bytes:
            for i in range(len(self.baudot)):
                if self.baudot[i]["code"] == byte:
                    retStr += self.baudot[i]["char"]
                    break

        return retStr


    def plainToBytes(self, plain):
        bits = []

        for c in list(plain):
            for i in range(len(self.baudot)):
                if self.baudot[i]["char"] == c.upper():
                    bits.append(self.baudot[i]["code"])
                    break

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

