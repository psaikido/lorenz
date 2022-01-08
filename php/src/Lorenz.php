<?php declare(strict_types=1);
namespace Lorenz;

use \Exception;

class Lorenz
{
    public $debug = false;

    public $baudot = [
        " " => "00100",
        "." => "00010",
        "!" => "11111",
        "?" => "00000",
        "-" => "01000",
        "&" => "11011",
        "A" => "00011",
        "B" => "11001",
        "C" => "01110",
        "D" => "01001",
        "E" => "00001",
        "F" => "01101",
        "G" => "11010",
        "H" => "10100",
        "I" => "00110",
        "J" => "01011",
        "K" => "01111",
        "L" => "10010",
        "M" => "11100",
        "N" => "01100",
        "O" => "11000",
        "P" => "10110",
        "Q" => "10111",
        "R" => "01010",
        "S" => "00101",
        "T" => "10000",
        "U" => "00111",
        "V" => "11110",
        "W" => "10011",
        "X" => "11101",
        "Y" => "10101",
        "Z" => "10001",
    ];

    public $chiOne = 41;
    public $chiTwo = 31;
    public $alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];

    // chi wheels
    // 41, 31, 29, 26, and 23
    // psi wheels
    // 43, 47, 51, 53, and 59
    // mu wheels
    // 37 and 61

    public function code($plainText, $settings) {
        $plainBytes = $this->plainToBytes($plainText);
        $keyBytes = $this->plainToBytes($this->makeKeyStream($settings, strlen($plainText)));
        $cipherBytes = $this->bitwiseEncode($plainBytes, $keyBytes);
        $cipherText = $this->bytesToPlain($cipherBytes);

        $plainTextAr = str_split($plainText);

        if ($this->debug) {
            echo PHP_EOL;

            for ($x = 0; $x < strlen($plainText); $x++) {
                $pt = $plainBytes[$x];
                $ltr = $plainTextAr[$x];

                $kb = $keyBytes[$x];
                $kbLtr = array_search($kb, $this->baudot);

                $cb = $cipherBytes[$x];
                $cbLtr = array_search($cb, $this->baudot);

                echo "x: $x $ltr=$pt $kbLtr=$kb $cbLtr=$cb" . PHP_EOL;
            }
        }
        
        return $cipherText;
    }

    public function plainToBytes($plain) {
        $bits = [];

        foreach (str_split($plain) as $c) {
            try {
                $bits[] = $this->baudot[strtoupper($c)];
            } catch (Exception $e) {
                return $e->getMessage();
            }
        }

        return $bits;
    }

    public function bytesToPlain($cipherBytes) {
        $retStr = '';

        foreach ($cipherBytes as $fiveb) {
            $retStr .= array_search($fiveb, $this->baudot);
        }

        return $retStr;
    }

    public function xorBits($i, $j) {
        return $i === $j ? '0' : '1';
    }

    public function xorBytes($a, $b) {
        $tmpStr = '';

        for ($x = 0; $x < sizeof($a); $x++) {
            $tmpStr .= $this->xorBits($a[$x], $b[$x]);
        }

        return $tmpStr;
    }

    public function bitwiseEncode($plainBytes, $keyBytes) {
        $retA = [];
        $tmpStr = '';

        for ($x = 0; $x < sizeof($plainBytes); $x++) {
            $plainFiveBitsAr = str_split($plainBytes[$x]);
            $keyFiveBitsAr = str_split($keyBytes[$x]);

            $tmpStr = $this->xorBytes($plainFiveBitsAr, $keyFiveBitsAr);

            $retA[] = $tmpStr;
            $tmpStr = '';
        }

        return $retA;
    }

    public function generatePlainKey($magicKey, $plainText) {
        $retStr = '';
        $y = 0;

        $magicAr = str_split($magicKey);

        for ($x = 0; $x < strlen($plainText); $x++) {
            $retStr .= $magicAr[$y++];

            if ($y >= sizeof($magicAr)) {
                $y = 0;
            }
        }

        return $retStr;
    }

    public function makeKeyStream($settings, $keyLength) {
        $retStr = '';
        $y = $z = 0;

        $chiOneAr = $this->makeChiArray($this->chiOne, $settings[0]);
        $chiTwoAr = $this->makeChiArray($this->chiTwo, $settings[1]);

        for ($x = 0; $x < $keyLength; $x++) {
            $y = $y >= $this->chiOne - 1 ? $y = 0 : $y + 1;
            $z = $z >= $this->chiTwo - 1? $z = 0 : $z + 1;
            $chiOneByte = $chiOneAr[$y][1];
            $chiTwoByte = $chiTwoAr[$z][1];
            $xorProduct = $this->xorBytes(str_split($chiOneByte), str_split($chiTwoByte));
            $resultantLtr = array_search($xorProduct, $this->baudot);
            $retStr.= $resultantLtr;
        }

        return $retStr;
    }

    public function makeChiArray($upperLimit, $startingPos) {
        $chiAr = [];
        $y = $startingPos;

        for ($x = 0; $x < $upperLimit; $x++) {
            $y = $y >= 25 ? $y = 0 : $y + 1;

            $chiAr[] = [
                $this->alphabet[$y],
                $this->baudot[$this->alphabet[$y]]
            ];
        }

        return $chiAr;
    }
}

/*
$thing = new Lorenz;
//            SPIGWOMBLESPIGWOMBLESPIGWOMBLESPIGWOMBLE
//$magicKey = "SPIGWOMBLE";

$plainText = "THESE VIOLENT DELIGHTS HAVE VIOLENT ENDS";
$cipherText= "Y.U!LM.!RW GPVGBC!-YYW.CTIXXNUX UPAMXY& ";

echo $thing->code($plainText, [3,19]);
//echo $thing->makeKeyStream($plainText, [1,25]);
echo "\n";
 */
