/* Javascript for Blog form. */

var author_toggle = function() {
    var author = document.getElementById("div_id_author");
    if (this.value == "") {
        author.style.display = "block";
    }
    else {
        author.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    var fund = document.getElementById("id_fund");
    fund.addEventListener("change", author_toggle);
}, false);
