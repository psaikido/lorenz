<?php declare(strict_types=1);
namespace Enigma;

use \Exception;

class Enigma
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

    public function code($plainText, $magicKey) {
        $plainBytes = $this->plainToBytes($plainText);
        $keyBytes = $this->plainToBytes($this->generatePlainKey($magicKey, $plainText));
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

    public function bitwiseEncode($plainBytes, $keyBytes) {
        $retA = [];
        $tmpStr = '';

        for ($x = 0; $x < sizeof($plainBytes); $x++) {
            $plainFiveBitsAr = str_split($plainBytes[$x]);
            $keyFiveBitsAr = str_split($keyBytes[$x]);

            for ($y = 0; $y < sizeof($plainFiveBitsAr); $y++) {
                $tmpStr .= $this->xorBits($plainFiveBitsAr[$y], $keyFiveBitsAr[$y]);
            }

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
}

/*
$thing = new Enigma;
//            SPIGWOMBLESPIGWOMBLESPIGWOMBLESPIGWOMBLE
$magicKey = "SPIGWOMBLE";

$plainText = "THESE VIOLENT DELIGHTS HAVE VIOLENT ENDS";
$cipherText= "Y.U!LM.!RW GPVGBC!-YYW.CTIXXNUX UPAMXY& ";

echo $thing->code($plainText, $magicKey);
echo "\n";
 */
