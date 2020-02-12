<!DOCTYPE html>
<html>
    <head>
        <title>TrafficAccidents by //Nickname</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" type="text/css" href="style.css">
        <script type="text/javascript" src="https://cdn.jsdelivr.net/jquery/latest/jquery.min.js"></script>
        <script type="text/javascript" src="https://cdn.jsdelivr.net/momentjs/latest/moment.min.js"></script>
        <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css" />
    </head>
    <body>
        <header>
            <h1>//nickname</h1>
        </header>
        <main>
            <form name="search" action="" method="GET">
                <input type="text" name="daterange">
                <input type="text" name="search">
                <input type="submit">
            </form>
            <script>
                $('input[name="daterange"]').daterangepicker({
                    "locale": {
                        "format": "DD.MM.YYYY",
                        "separator": "-",
                        "applyLabel": "Выбрать",
                        "cancelLabel": "Отмена",
                        "fromLabel": "От",
                        "toLabel": "до",
                        "daysOfWeek": ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
                        "monthNames": [
                            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
                        ],
                        "firstDay": 1
                    }
                });
                var gets = (function() {
                    var a = window.location.search;
                    var b = new Object();
                    a = a.substring(1).split("&");
                    for (var i = 0; i < a.length; i++) {
                        c = a[i].split("=");
                        b[c[0]] = c[1];
                    }
                    return b;
                })();
                if (gets.length != 0) {
                    if (gets["daterange"]) {
                        document.forms["search"]["daterange"].value = gets["daterange"];
                    }
                    if (gets["search"]) {
                        document.forms["search"]["search"].value = decodeURI(gets["search"]);
                    }
                }
            </script>
            <table id="results">
                <tr>
                    <th>Дата</th>
                    <th>Место</th>
                    <th>Тональность</th>
                    <th>Погибшие</th>
                    <th>Пострадавшие</th>
                    <th>Заголовок</th>
                    <th>Статья</th>
                    <th>Ссылка</th>
                </tr>
                <?php
                function test_input($data) {
                    $data = trim($data);
                    $data = stripslashes($data);
                    $data = htmlspecialchars($data);
                    return $data;
                }

                $servername = "localhost";
                $username = "webuser";
                $password = "P@ssw0rd"; # Test password
                $dbname = "TrafficAccidents";

                $conn = new mysqli($servername, $username, $password, $dbname);
                $conn->set_charset('utf8');
                if($conn->connect_error) {
                    die("Connection failed: " . $conn->connect_error);
                }

                date_default_timezone_set('Europe/Moscow');
                $date = date('Y-m-d', time());
                $sqlnews = "SELECT * FROM News WHERE Date = '$date'";
                $sqlgroup = "SELECT * FROM Groups WHERE Date = '$date'";
                $search = "";
                if ($_GET["daterange"] != "") {
                    list($firstdate, $lastdate) = explode("-", test_input($_GET["daterange"]));
                    $firstdate = explode(".", $firstdate);
                    $firstdate = $firstdate[2] . "-" . $firstdate[1] . "-" . $firstdate[0];
                    $lastdate = explode(".", $lastdate);
                    $lastdate = $lastdate[2] . "-" . $lastdate[1] . "-" . $lastdate[0];
                    $search = test_input($_GET["search"]);
                    $sqlgroupslist = "SELECT DISTINCT GroupID FROM News WHERE Date BETWEEN '$firstdate' AND '$lastdate'";
                    $sqlnews = "SELECT * FROM News WHERE Date BETWEEN '$firstdate' AND '$lastdate'";
                    $sqlgroup = "SELECT * FROM Groups WHERE Date BETWEEN '$firstdate' AND '$lastdate'";
                }
                if($search == "") {
                    $grouplist = $conn->query($sqlgroup);
                    while($group = $grouplist->fetch_assoc()) {
                        echo "<tr><th colspan=8 class=\"newsgroup\">" . $group["Title"] . "</th></tr>";
                        $newslist = $conn->query($sqlnews . " AND GroupID = " . $group["ID"]);
                        while($news = $newslist->fetch_assoc()) {
                            echo "<tr><td>" . $news["Date"] . "</td><td>" . $news["Location"] . "</td><td>" . number_format($news["Tone"]*100, 2) . "%" . "</td><td>" . $news["Killed"] . "</td><td>" . $news["Injured"] . "</td><td>" . $news["Title"] . "</td><td>" . $news["Article"] . "</td><td><a href=\"" . $news["Link"] . "\">Ссылка</a></td></tr>";
                        }
                    }
                    echo "<tr><th colspan=8 class=\"newsgroup\">Не сгруппировано</th></tr>";
                    $newslist = $conn->query($sqlnews . " AND GroupID = -1");
                    while($news = $newslist->fetch_assoc()) {
                        echo "<tr><td>" . $news["Date"] . "</td><td>" . $news["Location"] . "</td><td>" . number_format($news["Tone"]*100, 2) . "%" . "</td><td>" . $news["Killed"] . "</td><td>" . $news["Injured"] . "</td><td>" . $news["Title"] . "</td><td>" . $news["Article"] . "</td><td><a href=\"" . $news["Link"] . "\">Ссылка</a></td></tr>";
                    }
                }
                else {
                    $grouplist = $conn->query($sqlgroupslist . " AND (Location LIKE '%$search%' OR Title LIKE '%$search%' OR Article LIKE '%$search%') AND GroupID <> -1 ORDER BY GroupID");
                    while($groupid = $grouplist->fetch_assoc()) {
                        $groupq = $conn->query("SELECT * FROM Groups WHERE ID = " . $groupid["GroupID"]);
                        while($group = $groupq->fetch_assoc()) {
                            echo "<tr><th colspan=8 class=\"newsgroup\">" . $group["Title"] . "</th></tr>";
                            $newslist = $conn->query($sqlnews . " AND GroupID = " . $group["ID"]);
                            while($news = $newslist->fetch_assoc()) {
                                echo "<tr><td>" . $news["Date"] . "</td><td>" . $news["Location"] . "</td><td>" . number_format($news["Tone"]*100, 2) . "%" . "</td><td>" . $news["Killed"] . "</td><td>" . $news["Injured"] . "</td><td>" . $news["Title"] . "</td><td>" . $news["Article"] . "</td><td><a href=\"" . $news["Link"] . "\">Ссылка</a></td></tr>";
                            }
                        }
                    }
                    echo "<tr><th colspan=8 class=\"newsgroup\">Не сгруппировано</th></tr>";
                    $newslist = $conn->query($sqlnews . " AND (Location LIKE '%$search%' OR Title LIKE '%$search%' OR Article LIKE '%$search%') AND GroupID = -1");
                    while($news = $newslist->fetch_assoc()) {
                        echo "<tr><td>" . $news["Date"] . "</td><td>" . $news["Location"] . "</td><td>" . number_format($news["Tone"]*100, 2) . "%" . "</td><td>" . $news["Killed"] . "</td><td>" . $news["Injured"] . "</td><td>" . $news["Title"] . "</td><td>" . $news["Article"] . "</td><td><a href=\"" . $news["Link"] . "\">Ссылка</a></td></tr>";
                    }
                }
                $conn->close();
                ?>
            </table>
        </main>
        <footer>
            <p>Создано <b class="brand">//nickname</b></p>
        </footer>
    </body>
</html>