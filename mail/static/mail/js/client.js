function showMail(e){
    document.getElementById("mailList").style.display = "none";
    document.getElementById("mailView").style.display = "block";
    document.getElementById("returnToListBtn").style.display = "block";
    document.getElementById("mailViewTitle").innerHTML = "HI";
    document.getElementById("mailViewContent").innerHTML = "BYE";
}
function showList(e){
    document.getElementById("mailList").style.display = "block";
    document.getElementById("mailView").style.display = "none";
    document.getElementById("returnToListBtn").style.display = "none";
}