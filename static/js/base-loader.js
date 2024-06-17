// function loading() {
//     var loading = document.getElementById("loading");
//     var content = document.getElementById("content");
//
//     loading.style.display = "block";
//     content.style.display = "none";
// }
document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        document.querySelector("body").style.visibility = "hidden";
        document.querySelector("#loader").style.visibility = "visible";
    } else {
        document.querySelector("#loader").style.display = "none";
        document.querySelector("body").style.visibility = "visible";
    }
};