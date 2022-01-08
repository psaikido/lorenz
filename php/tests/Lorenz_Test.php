<?php declare(strict_types=1);
namespace LorenzTest;

use PHPUnit\Framework\TestCase;
use Lorenz\Lorenz;

class Lorenz_Test extends TestCase {
    private function revTest($actual, $expected) {
        $this->assertEquals($expected, $actual);
    }

    public function testBasics() {
        $class = new Lorenz;
        $magicKey = 'SPIGWOMBLE';

        $text0 = 'ABC';
        $cipherText0 = '&JD';

        $text1 = 'abc';
        $cipherText1 = 'HQM';

        $text2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        $cipherText2 = 'XDHYBIFJAFMAR?-RLXD&E&B.E.';

        $text3 = 'OM AH HUM BENZA GURU PEMA SIDDHI HUM';
        $cipherText3 = 'DUTHQCVMCQVNQLBKOBIOCC.KPKHXXVQ!QRAI';

        $text4 = 'THESE VIOLENT DELIGHTS HAVE VIOLENT ENDS AND IN THEIR TRIUMPH DIE LIKE FIRE AND POWDER WHICH AS THEY KISS CONSUME';
        $cipherText4 = 'O.XTNZLSHMVBL&N.HKIRVGGW.DDL.WYDCYW?MZATLUZUHL.SF&HZWDV..YIEWNJLYBY?GUVRZCR.VRBT?Y!O?JXGE-ROYU.B ?XNDU JG.PIZX!SX';

        $this->revTest($class->code($text0, [9,22]), $cipherText0);
        $this->revTest($class->code($cipherText0, [9,22]), $text0);
        $this->revTest($class->code($cipherText0, [8,22]), 'CXW');
        $this->revTest($class->code($cipherText0, [9,23]), 'FZR');
        
        $this->revTest($class->code($text1, [5,6]), $cipherText1);
        $this->revTest($class->code($cipherText1, [5,6]), strtoupper($text1));
        $this->revTest($class->code($text2, [20,1]), $cipherText2);
        $this->revTest($class->code($cipherText2, [20,1]), $text2);
        $this->revTest($class->code($text3, [6,9]), $cipherText3);
        $this->revTest($class->code($cipherText3, [6,9]), $text3);
        $this->revTest($class->code($text4, [9,0]), $cipherText4);
        $this->revTest($class->code($cipherText4, [9,0]), $text4);
    }

    public function test_plainToBytes() {
        $class = new Lorenz;
        $this->revTest($class->plainToBytes('E'), ['00001']);
        $this->revTest($class->plainToBytes(' '), ['00100']);
        $this->revTest($class->plainToBytes('.'), ['00010']);
        $this->revTest($class->plainToBytes(''), 'Undefined index: ');
        $this->revTest($class->plainToBytes('*'), 'Undefined index: *');
        $this->revTest($class->plainToBytes('['), 'Undefined index: [');
        $this->revTest($class->plainToBytes('3'), 'Undefined offset: 3');
    }

    public function test_bytesToPlain() {
        $class = new Lorenz;
        $this->revTest($class->bytesToPlain(['00001']), 'E');
        $this->revTest($class->bytesToPlain(['00100']), ' ');
        $this->revTest($class->bytesToPlain(['00010']), '.');
        $this->revTest($class->bytesToPlain(['4']), '');
        $this->revTest($class->bytesToPlain(['elf']), '');
    }

    public function test_xorBits() {
        $class = new Lorenz;
        
        $this->revTest($class->xorBits('0', '0'), '0');
        $this->revTest($class->xorBits('1', '1'), '0');
        $this->revTest($class->xorBits('0', '1'), '1');
        $this->revTest($class->xorBits('1', '0'), '1');
        $this->revTest($class->xorBits('', '0'), '1');
    }

    public function test_xorBytes() {
        $class = new Lorenz;
        
        $this->revTest($class->xorBytes([1,0,0,0,0], [0,0,0,0,1]), '10001');
        $this->revTest($class->xorBytes([0,1,0,1,0], [1,0,1,0,1]), '11111');
        $this->revTest($class->xorBytes([1,1,1,1,1], [1,0,1,0,1]), '01010');
    }

    public function test_bitwiseEncode() {
        $class = new Lorenz;
        
        $this->revTest($class->bitwiseEncode(['10000'],['10011']), ['00011']);
        $this->revTest($class->bitwiseEncode(['10100'],['10011']), ['00111']);
        $this->revTest($class->bitwiseEncode(['10111'],['10110']), ['00001']);
    }

    public function test_makeKeyStream() {
        $class = new Lorenz;

        $key0 = 'N!ROAWYJZ&';
        $key1 = 'N!ROAWYJZ&HQARR&LWUF&AGJ.VN!ROAKSSLE&XE..!SIWZPNTMSQNJISR!HW';
        $key2 = 'N!ROAWYJZ&HQARR&LWUF&AGJ.VN!ROAKSSLE&XE..!SIWZPNTMSQNJISR!HWVTINP-FTK &BM!DBWV GKMMVC!VUEQ-PMDX&KBA XXRYPGA!YP!PU! EYMKDX&KQ&O.HHXUIYIGUQ JIXITHPFLKT &O.HHEQ-PMYFYNF-.C!IOVXOOBM!- QTE UX- LGQU-NQCLF X';
        $key3 = '! EYMKDX&K';

        $this->revTest($class->makeKeyStream([1,24], strlen($key0)), $key0);
        $this->revTest($class->makeKeyStream([1,24], strlen($key1)), $key1);
        $this->revTest($class->makeKeyStream([1,24], strlen($key2)), $key2);
        $this->revTest($class->makeKeyStream([18,6], strlen($key3)), $key3);
    }

    public function test_makeChiArray() {
        $class = new Lorenz;

        $this->revTest($class->makeChiArray(3,0), [
            ['A', '00011'],
            ['B', '11001'],
            ['C', '01110'],
        ]);
    }
}
