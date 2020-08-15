//var i = 0;

function ContestTimer() {
    //i = i + 1;
    postMessage(["countdown",Date()]);
    setTimeout("ContestTimer()",1000);
}

onmessage = function(event) {
    if (event.data[0] == "start"){
        ContestTimer();
    }

}

