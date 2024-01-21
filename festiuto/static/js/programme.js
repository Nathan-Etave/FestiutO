function toggle_concert(id) {
    console.log(id);
    var element = document.getElementById(id);
    if (element.style.display == "none") {
        element.style.display = "block";
        element.style.backgroundColor = "";
    } else {
        element.style.display = "none";
        element.style.backgroundColor = "#4b50b4";
    }
}