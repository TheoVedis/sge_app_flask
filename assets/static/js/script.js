function openNav() {
    /* Documentation
    Cette fonction a pour but d'ouvrir et fermer le menu lattéral
    ainsi que décaler le contenu de la page principal vers la droite
    */

    var val = document.getElementById("sideMenu-btn").getAttribute("isOpen");

    if (val == undefined) {
        return;
    }
    if (val == "false") {
        document.getElementById("sideMenu").style.width = "350px";
        document.getElementById("page-content").style.marginLeft = "350px";
        document.getElementById("sideMenu-btn").style.transform = "scaleX(-1)";
        document.getElementById("sideMenu-btn").setAttribute("isOpen", "true");
        return;
    } else {
        document.getElementById("sideMenu").style.width = "0px";
        document.getElementById("page-content").style.marginLeft = "0px";
        document.getElementById("sideMenu-btn").style.transform = "scaleX(1)";
        document.getElementById("sideMenu-btn").setAttribute("isOpen", "false");
        return;
    }
}

function toArray(obj) {
    var array = [];

    for (var i = obj.length >>> 0; i--; ) {
        array[i] = obj[i];
    }
    return array;
}

$(document).ready(function () {
    $("#filtre-btn").click(function (e) {
        var val = $(".select2-selection__choice").map(function () {
            return this.title;
        });

        val = toArray(val);

        if (val.length == 0) {
            return;
        }

        $.ajax({
            url: "/page/test",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                value: val,
            }),
            succes: function (result) {
                alert("SUCCES");
            },
            error: function (result) {
                alert("ERROR");
            },
        });
    });
});
