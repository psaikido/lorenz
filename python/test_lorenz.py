#! /usr/bin/python

from lorenz import Lorenz

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
            ['A', '00011'],
            ['B', '11001'],
            ['C', '01110'],
            ['D', '01001'],
            ['E', '00001']
        ]

def test_makeKeyStream():
    lorenz = Lorenz()

    key0 = "N!ROAWYJZ'"
    key1 = "N!ROAWYJZ'HQARR'LWUF'AGJ.VN!ROAKSSLE'XE..!SIWZPNTMSQNJISR!HW"
    key2 = "N!ROAWYJZ'HQARR'LWUF'AGJ.VN!ROAKSSLE'XE..!SIWZPNTMSQNJISR!HWVTINP,FTK 'BM!DBWV GKMMVC!VUEQ,PMDX'KBA XXRYPGA!YP!PU! EYMKDX'KQ'O.HHXUIYIGUQ JIXITHPFLKT 'O.HHEQ,PMYFYNF,.C!IOVXOOBM!, QTE UX, LGQU,NQCLF X"
    key3 = "! EYMKDX'K"

    assert lorenz.makeKeyStream([1,24], len(key0)) == key0
    assert lorenz.makeKeyStream([1,24], len(key1)) == key1
    assert lorenz.makeKeyStream([1,24], len(key2)) == key2
    assert lorenz.makeKeyStream([18,6], len(key3)) == key3

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
    cipherText0 = "'JD"

    text1 = "abc"
    cipherText1 = "HQM"

    text2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cipherText2 = "XDHYBIFJAFMAR?,RLXD'E'B.E."

    text3 = "OM AH HUM BENZA GURU PEMA SIDDHI HUM"
    cipherText3 = "DUTHQCVMCQVNQLBKOBIOCC.KPKHXXVQ!QRAI"

    text4 = "THESE VIOLENT DELIGHTS HAVE VIOLENT ENDS AND IN THEIR TRIUMPH DIE LIKE FIRE AND POWDER WHICH AS THEY KISS CONSUME"
    cipherText4 = "O.XTNZLSHMVBL'N.HKIRVGGW.DDL.WYDCYW?MZATLUZUHL.SF'HZWDV..YIEWNJLYBY?GUVRZCR.VRBT?Y!O?JXGE,ROYU.B ?XNDU JG.PIZX!SX"

    text5 = "plain*text"
    text6 = "plain[text"

    text7 = "ABCDE"
    cipherText7 = "CN.RF"

    assert lorenz.code(text0, [9,22]) == cipherText0
    assert lorenz.code(text0, [9,22]) == cipherText0
    assert lorenz.code(cipherText0, [9,22]) == text0
    assert lorenz.code(cipherText0, [8,22]) == "CXW"
    assert lorenz.code(cipherText0, [9,23]) == "FZR"
    assert lorenz.code(text1, [5,6]) == cipherText1
    assert lorenz.code(cipherText1, [5,6]) == text1.upper()
    assert lorenz.code(text2, [20,1]) == cipherText2
    assert lorenz.code(cipherText2, [20,1]) == text2
    assert lorenz.code(text3, [6,9]) == cipherText3
    assert lorenz.code(cipherText3, [6,9]) == text3
    assert lorenz.code(text4, [9,0]) == cipherText4
    assert lorenz.code(cipherText4, [9,0]) == text4
    assert lorenz.code(text5, [9,10]) == "Dissallowed character: *" 
    assert lorenz.code(text6, [9,10]) == "Dissallowed character: [" 
    #assert lorenz.code(text7, [1,1]) == cipherText7
    #assert lorenz.code(cipherText7, [13,4]) == text7
