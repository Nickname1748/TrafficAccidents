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
        <h1>//Nickname</h1>
        <form action="" method="GET">
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
        </script>
        <table>
            <tr>
                <th>Date</th>
                <th>Location</th>
                <th>Title</th>
                <th>Article</th>
                <th>Link</th>
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

            $sql = "SELECT * FROM News";
            if ($_SERVER["REQUEST_METHOD"] == "GET") {
                list($firstdate, $lastdate) = explode("-", test_input($_GET["daterange"]));
                $firstdate = explode(".", $firstdate);
                $firstdate = $firstdate[2] . "-" . $firstdate[1] . "-" . $firstdate[0];
                $lastdate = explode(".", $lastdate);
                $lastdate = $lastdate[2] . "-" . $lastdate[1] . "-" . $lastdate[0];
                echo $firstdate . " " . $lastdate;
                $search = test_input($_GET["search"]);
                if ($search == "") {
                    $sql = "SELECT * FROM News WHERE Date BETWEEN '$firstdate' AND '$lastdate'";
                }
                else {
                    $sql = "SELECT * FROM News WHERE (Date BETWEEN '$firstdate' AND '$lastdate') AND (Title LIKE '%$search%' OR Article LIKE '%$search%')";
                }
            }
            $result = $conn->query($sql);
            if ($result->num_rows > 0) {
                while($row = $result->fetch_assoc()) {
                    echo "<tr><td>" . $row["Date"] . "</td><td>" . $row["Location"] . "</td><td>" . $row["Title"] . "</td><td>" . $row["Article"] . "</td><td><a href=\"" . $row["Link"] . "\">Link</a></td></tr>";
                }
            }
            $conn->close();
            ?>
        </table>
    </body>
</html>