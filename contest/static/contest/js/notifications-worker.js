var username;

function GetLatestNotifications() {
    var url = "https://api4qubit.pythonanywhere.com/contest/notifications/for/"+username+"/";
    var output;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.timeout = 120000;
    xhr.onload = function (e) {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          output = JSON.parse(xhr.responseText);
          if (output.length != 0){
              postMessage(["response",output]);
          } else {
              close();
          }
        }
      }
    };
    xhr.send(null);
    setTimeout("GetLatestNotifications()",10000);
}

onmessage = function(event) {
    if (event.data[0] == "start"){
        username = event.data[1];
        GetLatestNotifications();
    }
}

