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
        if($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $sql = "SELECT * FROM News";
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) {
                echo "id: " . $row["ID"]. " - Title: " . $row["Title"]. " " . $row["Article"]. "<br>";
            }
        } else {
            echo "0 results";
        }
        $conn->close();
        /*if ($_SERVER["REQUEST_METHOD"] == "GET") {
            $daterange = test_input($_GET["daterange"]);
            $search = test_input($_GET["search"]);
        }*/
        ?>
    </body>
</html>