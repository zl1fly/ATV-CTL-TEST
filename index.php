<?PHP

$user_name = "user";
$password = "password";
$database = "database";
$server = "127.0.0.1";

$db_handle = mysql_connect($server, $user_name, $password);
$db_found = mysql_select_db($database, $db_handle);

if ($db_found) {

$SQL = "select * from cabin_values order by time DESC limit 1";
$result = mysql_query($SQL);

while ( $db_field = mysql_fetch_assoc($result) ) {

print "Temperature : " . $db_field['temp'] . "C <BR>";
print "Humidity : " . $db_field['humidity'] . "% <BR>";

}

mysql_close($db_handle);

}
else {

print "Database NOT Found ";
mysql_close($db_handle);

}

?>