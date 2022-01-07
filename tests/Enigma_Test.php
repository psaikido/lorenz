<?php declare(strict_types=1);
namespace EnigmaTest;

use PHPUnit\Framework\TestCase;
use Enigma\Enigma;

class Enigma_Test extends TestCase {
    private function revTest($actual, $expected) {
        $this->assertEquals($expected, $actual);
    }

    public function testBasics() {
        $class = new Enigma;
        $magicKey = "SPIGWOMBLE";

        $text0 = "ABC";
        $cipherText0 = "IK-";

        $text1 = "abc";
        $cipherText1 = "IK-";

        $text2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        $cipherText2 = "IK-WLYIFHRR GPJCJWQZ.-YUID";

        $text3 = "OM AH HUM BENZA GURU PEMA SIDDHI HUM";
        $cipherText3 = "XR.BUM-VCSMQRJTMIVOIE?UITMB!&-ZT.CH ";

        $text4 = "THESE VIOLENT DELIGHTS HAVE VIOLENT ENDS AND IN THEIR TRIUMPH DIE LIKE FIRE AND POWDER WHICH AS THEY KISS CONSUME";
        $cipherText4 = "Y.U!LM.!RW GPVGBC!-YYW.CTIXXNUX UPAMXY& EYRWQVTX.Y TNVALGVCQZLKMLMC!X?E&?TLM!Y&SWCYWLLORIUJ..BPMNFWHEB?!PMLEV .RU";

        $this->revTest($class->code($text0, $magicKey), $cipherText0);
        $this->revTest($class->code($cipherText0, $magicKey), $text0);
        $this->revTest($class->code($text1, $magicKey), $cipherText1);
        $this->revTest($class->code($cipherText1, $magicKey), strtoupper($text1));
        $this->revTest($class->code($text2, $magicKey), $cipherText2);
        $this->revTest($class->code($cipherText2, $magicKey), $text2);
        $this->revTest($class->code($text3, $magicKey), $cipherText3);
        $this->revTest($class->code($cipherText3, $magicKey), $text3);
        $this->revTest($class->code($text4, $magicKey), $cipherText4);
        $this->revTest($class->code($cipherText4, $magicKey), $text4);
    }

    public function test_plainToBytes() {
        $class = new Enigma;
        $this->revTest($class->plainToBytes("E"), ["00001"]);
        $this->revTest($class->plainToBytes(" "), ["00100"]);
        $this->revTest($class->plainToBytes("."), ["00010"]);
        $this->revTest($class->plainToBytes(""), "Undefined index: ");
        $this->revTest($class->plainToBytes("*"), "Undefined index: *");
        $this->revTest($class->plainToBytes("["), "Undefined index: [");
        $this->revTest($class->plainToBytes("3"), "Undefined offset: 3");
    }

    public function test_bytesToPlain() {
        $class = new Enigma;
        $this->revTest($class->bytesToPlain(["00001"]), "E");
        $this->revTest($class->bytesToPlain(["00100"]), " ");
        $this->revTest($class->bytesToPlain(["00010"]), ".");
        $this->revTest($class->bytesToPlain(["4"]), "");
        $this->revTest($class->bytesToPlain(["elf"]), "");
    }

    public function test_xorBits() {
        $class = new Enigma;
        
        $this->revTest($class->xorBits('0', '0'), '0');
        $this->revTest($class->xorBits('1', '1'), '0');
        $this->revTest($class->xorBits('0', '1'), '1');
        $this->revTest($class->xorBits('1', '0'), '1');
        $this->revTest($class->xorBits('', '0'), '1');
    }

    public function test_bitwiseEncode() {
        $class = new Enigma;
        
        $this->revTest($class->bitwiseEncode(["10000"],["10011"]), ["00011"]);
        $this->revTest($class->bitwiseEncode(["10100"],["10011"]), ["00111"]);
        $this->revTest($class->bitwiseEncode(["10111"],["10110"]), ["00001"]);
    }

    public function test_generatePlainKey() {
        $class = new Enigma;
        $magicKey = "MAGICKEY";

        $this->revTest($class->generatePlainKey($magicKey, "four"), "MAGI");
        $this->revTest($class->generatePlainKey($magicKey, "fourfourfour"), "MAGICKEYMAGI");
    }
}
