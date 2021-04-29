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

    <form action="file1.php" method="post">
        <img src="sergi.png" alt=""> <br>
        <input type="text" name="input_query" value="<a:0.2;b:0.3>"> <br> <br>
        <input type="submit" value="Search" name="search">
        <input type="submit" value="Generate Files" name="generate">
        <input type="submit" value="Delete Files" name="delete">
    </form>
    <br>
</body>

</html>

<?php

$numDocs = 0;
$totalDocs = 10;

$alph = ['a', 'b', 'c', 'd', 'e', 'f'];


$TotalFreq = [];
$TotalProp = [];
$n = 500.0;

if (isset($_POST['generate'])) {

    while ($numDocs < $totalDocs) {

        //Create a file
        $myfile = fopen("webdict$numDocs.txt", "a+");

        $i = 0;
        $str = "";
        while ($i < $n) {
            $ranChar = $alph[rand(0, 5)];
            $str .= $ranChar;
            if ($i < ($n - 1)) {
                $str .= " ";
            }
            $i++;
        }
        fwrite($myfile, $str);
        fclose($myfile);

        $freqArray = array(
            "a" => 0,
            "b" => 0,
            "c" => 0,
            "d" => 0,
            "e" => 0,
            "f" => 0,
        );

        $myfile = fopen("webdict$numDocs.txt", "r");
        while (!feof($myfile)) {
            $char = fgetc($myfile);
            if ($char == ' ' || $char == '0') continue;
            $freqArray[$char]++;
        }

        array_push($TotalProp, $freqArray);

        foreach ($freqArray as $key => $value) {
            $value /= $n;
            $freqArray[$key] = $value;
        }

        fclose($myfile);
        array_push($TotalFreq, $freqArray);
        $numDocs++;
    }

    echo "<h1>Prop</h1>";
    for ($ii = 0; $ii < count($TotalFreq); $ii++) {
        print_r($TotalFreq[$ii]);
        echo "<br>";
    }

    echo "<h1>Freq</h1>";
    for ($ii = 0; $ii < count($TotalProp); $ii++) {
        print_r($TotalProp[$ii]);
        echo "<br>";
    }
}

if (isset($_POST['search'])) {

    while ($numDocs < $totalDocs) {

        $freqArray = array(
            "a" => 0,
            "b" => 0,
            "c" => 0,
            "d" => 0,
            "e" => 0,
            "f" => 0,
        );

        $myfile = fopen("webdict$numDocs.txt", "r");
        while (!feof($myfile)) {
            $char = fgetc($myfile);
            if ($char == ' ' || $char == '0') continue;
            $freqArray[$char]++;
        }

        // array_push($TotalProp, $freqArray);

        foreach ($freqArray as $key => $value) {
            $value /= $n;
            $freqArray[$key] = $value;
        }

        fclose($myfile);
        array_push($TotalProp, $freqArray);
        $numDocs++;
    }

    $query = htmlspecialchars($_POST['input_query']);
    $query = str_replace(array("&lt;", "&gt;"), "", $query);
    $arr = explode(";", $query);

    $queryArr = array(
        "a" => 0,
        "b" => 0,
        "c" => 0,
        "d" => 0,
        "e" => 0,
        "f" => 0,
    );
    for ($i = 0; $i < count($arr); $i++) {
        $temp = explode(":", $arr[$i]);
        $queryArr[$temp[0]] = (float)$temp[1];
    }

    $total = [];
    $j = 0;
    foreach ($queryArr  as $Qkey => $Qvalue) {
        for ($i = 0; $i < count($TotalProp); $i++) {
            $total[$i][$j] = $TotalProp[$i][$Qkey] * $queryArr[$Qkey];
        }
        $j++;
    }
    printDict($total);
}




if (isset($_POST['delete'])) {
    $numDocs = 0;
    $totalDocs = 10;
    while ($numDocs < $totalDocs) {
        unlink("webdict$numDocs.txt");
        $numDocs++;
    }
}

function printDict($total)
{
    $alph = ['a', 'b', 'c', 'd', 'e', 'f'];
    echo "<h1>Results</h1>";
    echo "<table style='width:100%;'>";
    $i = 0;
    foreach ($total as $key => $value) {
        echo "<tr>";
        echo "<th>";
        echo "Document $i";
        echo "</th>";
        foreach ($value as $keyChild => $valueChild) {
            echo "<td>$alph[$keyChild] = $valueChild; </td>";
        }
        $i++;
        echo "</tr>";
    }
    echo "</table>";
}
?>