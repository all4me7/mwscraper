let title = document.getElementById("idtitle");
let field1 = document.getElementById("idtag");
let field2 = document.getElementById("idattribute");
let field3 = document.getElementById("idvalue");


field1.addEventListener("input", () => {
    let field2 = document.getElementById("idattribute");
    if (field1.value.length > 0) {
        field2.removeAttribute("readonly")
    } else {
        field2.value = "";
        field3.value = "";
        field2.setAttribute("readonly", true);
        field3.setAttribute("readonly", true);
    }
})

field2.addEventListener("input", () => {
    let field3 = document.getElementById("idvalue");
    if (field2.value.length > 0) {
        field3.removeAttribute("readonly")
    } else {
        field3.setAttribute("readonly", true);
        field3.setAttribute("readonly", true)
    }
})

title.addEventListener("click", () => {
    document.getElementById("idurl").value = title.innerText.trim();
})

function empty() {
    let x;
    url = document.getElementById("idurl").value;
    if (url.length == 0) {
        alert("Invalid URL..");
        return false;
    } else {
        //
    }
}