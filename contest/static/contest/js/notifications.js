var cd = new Date();
for (var i = 0; i < localStorage.length; i++) {
    var key = localStorage.key(i);
    var value = localStorage.getItem(key);
    var thatd = new Date(JSON.parse(value));
    if (thatd < cd){
        localStorage.removeItem(key);
    }
}

var notification_allowed = false;

if (!("Notification" in window)) {
console.log("This browser does not support desktop notification");
}
else if (Notification.permission === "granted") {
var notification_allowed = true;
}
else if (Notification.permission !== 'denied' || Notification.permission === "default") {
Notification.requestPermission(function (permission) {
  if (permission === "granted") {
    var notification_allowed = true;
  }
});

}

function start(){
    var w;
    var response;
    w = new Worker("https://qubit.pythonanywhere.com/static/contest/js/notifications-worker.js");
    w.postMessage(["start",username]);
    w.onmessage = function(event) {
        if(event.data[0] == "response" ){
            response = event.data[1];
            for(var i = 0; i < response.length;i++ )
            {
                var contest = response[i];
                for(var j = 0; j < contest.notifications.length; j++ )
                {
                    var options = {
                          body: "برای مسابقه "+ contest.contest_name,
                          icon:"https://qubit.pythonanywhere.com/static/main/logo/Logo@4x.png",
                          dir : "rtl"
                    };
                    if(localStorage.getItem(contest.notifications[j].code) === null ){
                        var notification = new Notification(contest.notifications[j].title,options);
                        var d = new Date(contest.contest_end);
                        localStorage.setItem(contest.notifications[j].code,JSON.stringify(d));
                    }

                }

            }
        }
    };

}

var url = "https://api4qubit.pythonanywhere.com/contest/notifications/for/"+username+"/";
var output ;
var xhr = new XMLHttpRequest();
xhr.open("GET", url, true);
xhr.timeout = 120000;
xhr.onload = function (e) {
  if (xhr.readyState === 4) {
    if (xhr.status === 200) {
      output = JSON.parse(xhr.responseText);
      if (output.length != 0){
          start();
      }
    } else {
      console.error(xhr.statusText);
    }
  }
};
xhr.onerror = function (e) {
  console.error(xhr.statusText);
};
xhr.ontimeout = function(e) {
    console.error("Timeout!!")
};
xhr.send(null);