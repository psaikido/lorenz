#! /usr/bin/python

from lorenz_cls import Lorenz

def test_xorBits():
    lorenz = Lorenz()

    assert lorenz.xorBits('0', '0') == 0
    assert lorenz.xorBits('0', '1') == 1
    assert lorenz.xorBits('1', '0') == 1
    assert lorenz.xorBits('', '0') == 1


def test_xorBytes():
    lorenz = Lorenz()

    assert lorenz.xorBytes([1,0,0,0,0], [0,0,0,0,1]) == '10001'
    assert lorenz.xorBytes([0,1,0,1,0], [1,0,1,0,1]) == '11111'
    assert lorenz.xorBytes([1,1,1,1,1], [1,0,1,0,1]) == '01010'


def test_bitwiseEncode():
    lorenz = Lorenz()

    assert lorenz.bitwiseEncode(['10000'],['10011']) == ['00011']
    assert lorenz.bitwiseEncode(['10100'],['10011']) == ['00111']
    assert lorenz.bitwiseEncode(['10111'],['10110']) == ['00001']


def test_makeChiArray():
    lorenz = Lorenz()

    assert lorenz.makeChiArray(5,0) == [ 
            '00011',
            '11001',
            '01110',
            '01001',
            '00001'
        ]


def test_makeKeyStream():
    lorenz = Lorenz()

    key0 = "ABC"
    bytes0 = ['00011', '11001', '01110']

    key1 = "N!ROAWYJZ'"
    bytes1 = ['00110', '11010', '11010', '00111', '00101', '10010', '11111', '00111', '11011', '10110']

    assert lorenz.makeKeyStream([0,0,0], len(key0)) == bytes0


def test_bytesToPlain():
    lorenz = Lorenz()

    assert lorenz.bytesToPlain(['00001']) == "E"
    assert lorenz.bytesToPlain(['00100']) == " "
    assert lorenz.bytesToPlain(['00010']) == "."
    #assert lorenz.bytesToPlain(['4']) == "ValueError"
    #assert lorenz.bytesToPlain(['elf']) == ""


def test_plainToBytes():
    lorenz = Lorenz()

    assert lorenz.plainToBytes('E') == ['00001']
    assert lorenz.plainToBytes(' ') == ['00100']
    assert lorenz.plainToBytes('.') == ['00010']
    assert lorenz.plainToBytes('') == []
    #assert lorenz.plainToBytes('*') == 'Undefined index: *'
    #assert lorenz.plainToBytes('[') == 'Undefined index: ['
    #assert lorenz.plainToBytes('3') == 'Undefined offset: 3'

def test_code():
    lorenz = Lorenz()

    text0 = "ABC"
    cipherText0 = "QW!"

    text1 = "abc"
    cipherText1 = "?ZQ"

    text2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cipherText2 = "PIIDYV'MD,N HWY!AVTY,GHOY "

    text3 = "OM AH HUM BENZA GURU PEMA SIDDHI HUM"
    cipherText3 = "XE''SLL O?HDUYUMSNQ'Q?JC'Y?'PRZHOO!R"

    text4 = "THESE VIOLENT DELIGHTS HAVE VIOLENT ENDS AND IN THEIR TRIUMPH DIE LIKE FIRE AND POWDER WHICH AS THEY KISS CONSUME"
    cipherText4 = "XLGC!NUHQSTTWPPPL DO.P.SYAN.SPSCTICYFLGV'IMX?HDR!UODSVHULLAZHLOK?,PBHC!UJGNDZOSMOA,LS'G!ZKHJ,LWGXCHF XTFZF GXSDLQ"

    text5 = "plain*text"
    text6 = "plain[text"

    assert lorenz.code(text0, [9,22,13]) == cipherText0
    assert lorenz.code(cipherText0, [9,22,13]) == text0
    assert lorenz.code(cipherText0, [8,22,3]) == "J ,"
    assert lorenz.code(cipherText0, [10,25,3]) == "?AQ"
    assert lorenz.code(text1, [5,6,7]) == cipherText1
    assert lorenz.code(cipherText1, [5,6,7]) == text1.upper()
    assert lorenz.code(text2, [20,1,9]) == cipherText2
    assert lorenz.code(cipherText2, [20,1,9]) == text2
    assert lorenz.code(text3, [6,9,7]) == cipherText3
    assert lorenz.code(cipherText3, [6,9,7]) == text3
    assert lorenz.code(text4, [9,0,18]) == cipherText4
    assert lorenz.code(cipherText4, [9,0,18]) == text4
    assert lorenz.code(text5, [9,10,11]) == "Dissallowed character: *" 
    assert lorenz.code(text6, [9,10,11]) == "Dissallowed character: [" 
