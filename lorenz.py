#! /usr/bin/python

import re
import sys 

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

    def __init__(self):
        pass


    def run(self):
        while True:
            print("Enter Lorenz wheel settings as 3, comma separated numbers: ")

            settingsInput = input("settings: ").split(',')

            if len(settingsInput) != len(self.chiWheelLengths):
                print("3 inputs are needed")
                return

            #settings = [int(x) for x in settingsInput]
            settings = []
            for x in range(3):
                try:
                    cog = int(settingsInput[x])

                    if cog > self.chiWheelLengths[x]:
                        print(f"{cog} is too big")
                        return

                    settings.append(cog)
                except ValueError:
                    print("Integers only")
                    return

            self.getMsg(settings)
            

    def getMsg(self, settings):
        print("Enter ordinary letters, spaces and \",.?!'\"")
        res = self.code(input("msg? "), settings)
        print(f"Lorenz algo->\"{res}\"")
        sys.exit(0)


    def code(self, plainText, settings):
        for c in plainText.upper():
            found = False

            for i in range(len(self.baudot)):
                if self.baudot[i]["char"] == c:
                    found = True
                    break

            if found != True:
                return "Dissallowed character: " + c

        plainBytes = self.plainToBytes(plainText)
        keyBytes = self.makeKeyStream(settings, len(plainText))
        cipherBytes = self.bitwiseEncode(plainBytes, keyBytes)
        cipherText = self.bytesToPlain(cipherBytes)

        return cipherText


    def makeKeyStream(self, settings, keyLength):
        retStr = ""
        chiWheels = []
        firstTransform = []

        for x in range(len(self.chiWheelLengths)):
            wh = self.makeChiArray(self.chiWheelLengths[x], settings[x])
            chiWheels.append(wh)

        firstTransform = self.xorWheelPair(keyLength, chiWheels[0], chiWheels[1])
        secondTransform = self.xorWheelPair(keyLength, firstTransform, chiWheels[2])
        
        return secondTransform


    def xorWheelPair(self, keyLength, wheelOne, wheelTwo):
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
        y = startingPos % 26

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

if __name__ == "__main__":
    Lorenz().run()
