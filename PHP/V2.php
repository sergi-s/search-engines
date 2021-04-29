<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        body {
            margin: 50px 0px;
            padding: 0px;
            text-align: center;
        }

        form {
            display: inline-block;
        }

        table,
        th,
        td {
            border: 1px solid black;
        }
    </style>
</head>

<body>

    <form action="V2.php" method="post">
        <img src="sergi.png" alt=""> <br>
        <input type="text" name="input_query" value="<a:0.2;b:0.3>"> <br> <br>
        <input type="submit" value="Search" name="search">
        <input type="submit" value="Generate Files" name="generate">
        <!-- <input type="submit" value="Delete Files" name="delete"> -->
    </form>
    <br>
</body>

</html>
<?php
session_start();


if (isset($_POST['generate'])) {

    // CreateAlpha(10);
    CreateAlpha('j');

    GeneateFiles(3);
}

if (isset($_POST['search'])) {
    $queryArr = processQuery($_POST['input_query']);
    $Docs = $_SESSION['Docs'];

    //Statistical Model
    $DotProduct = statistical_models($Docs, $queryArr);
    echo "Statistical Model:<br>";
    for ($i = 0; $i < count($DotProduct); $i++) {
        echo "Document $i => Score: " . number_format((float)$DotProduct[$i], 5, '.', '') . "<br>";
    }

    TableGenerated($Docs);
}


function processQuery($query)
{
    $query = htmlspecialchars($query);
    $query = str_replace(array("&lt;", "&gt;"), "", $query);
    $arr = explode(";", $query);


    $queryArr = $_SESSION['alpha'];
    for ($i = 0; $i < count($arr); $i++) {
        $temp = explode(":", $arr[$i]);
        $queryArr[$temp[0]] = (float)$temp[1];
    }
    return $queryArr;
}


function statistical_models($Docs, $queryArr)
{
    $DotProduct = [];
    foreach ($Docs as $key => $arr2) {
        $sum = 0;
        foreach ($arr2['DocProp'] as $Dkey => $Dvalue) {
            $sum += $Dvalue * $queryArr[$Dkey];
        }
        $DotProduct[] = $sum;
    }

    return ($DotProduct);
}

function CreateAlpha($toChar)
{
    if (gettype($toChar) == 'string')
        $toChar = ord($toChar[0]) - ord('a') + 1;
    if ($toChar > 26) $toChar %= 26;
    $alpha = [];
    $alpha2 = [];
    for ($i = 0; $i < $toChar; $i++) {
        $char = chr(ord('a') + $i);
        $alpha2[$char] = 0;
        $alpha[$i] = $char;
    }
    $_SESSION['alphaDic'] = $alpha; // for refrence eg original
    $_SESSION['alpha'] = $alpha2; // for Counting
}

function GeneateFiles($numFiles)
{
    $Docs = [];
    for ($i = 0; $i < $numFiles; $i++) {
        $fileName = "Doc_$i.txt";

        if (file_exists($fileName)) unlink($fileName);

        $myFile = fopen($fileName, "a+");
        $fileSize = rand(100, 1000);
        $alpha = $_SESSION['alphaDic'];
        $str = " ";
        for ($j = 0; $j < $fileSize; $j++) {
            $str .= $alpha[rand(0, count($alpha) - 1)];
            $str .= ($j < $fileSize - 1) ? ' ' : '.';
        }
        fwrite($myFile, $str);
        fclose($myFile);

        $DocFre = getDocFreq($fileName);
        $DocProp = $DocFre;
        foreach ($DocProp as $key => $value) {
            $value /= $fileSize;
            $DocProp[$key] = $value;
        }
        $Docs[$i] = array("FileSize" => $fileSize, "DocFreq" => $DocFre, "DocProp" => $DocProp);
    }
    TableGenerated($Docs);
    $_SESSION['Docs'] = $Docs;
}

function TableGenerated($Docs)
{
    echo "<table style='width:100%;'>";
    foreach ($Docs as $Key => $Value) {
        echo "<tr>";
        echo "<th>";
        echo "Document $Key";
        echo "</th>";
        echo "<td>";
        echo "Size $Value[FileSize]";
        echo "</td>";

        echo "<td>";

        smallTable($Value['DocFreq'], $Value['DocProp']);

        echo "</td>";
        echo "</tr>";
    }
    echo "</table>";
}

function smallTable($DocFreq, $DocProp)
{
    echo "<table style='width:100%;'>";
    echo "<tr>";
    echo "<th>";
    echo "Char";
    echo "</th>";
    foreach ($DocFreq as $letter => $freq) {
        echo "<td>";
        echo "$letter";
        echo "</td>";
    }
    echo "</tr>";
    echo "<tr>";
    echo "<th>";
    echo "Freq";
    echo "</th>";
    foreach ($DocFreq as $letter => $freq) {
        echo "<td>";
        print_r($freq);
        echo "</td>";
    }
    echo "</tr>";
    echo "<tr>";
    echo "<th>";
    echo "Prop";
    echo "</th>";
    foreach ($DocProp as $letter => $freq) {
        echo "<td>";
        echo number_format((float)$freq, 4, '.', '');
        echo "</td>";
    }
    echo "</tr>";

    echo "</table>";
}

function getDocFreq($DocsName)
{
    $tempArr = $_SESSION['alpha'];
    $myfile = fopen($DocsName, "r");
    while (!feof($myfile)) {
        $char = fgetc($myfile);
        if ($char == ' ' || $char == '0' || $char == '.') continue;
        (isset($tempArr[$char])) ? $tempArr[$char]++ : $tempArr[$char] = 1;
    }
    return $tempArr;
}

?>