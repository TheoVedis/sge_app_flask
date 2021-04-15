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
    // Initialise le selecteur de date
    $("#picker").daterangepicker({
        autoApply: false,
        timePicker: false,
        startDate: "04/12/2019",
        endDate: "05/12/2019",
        locale: {
            format: "DD/MM/YYYY",
            applyClass: "btn-small btn-primary",
            separator: " - ",
            applyLabel: "OK",
            fromLabel: "De",
            toLabel: "à",
            customRangeLabel: "custom",
            daysOfWeek: ["Di", "Lu", "Ma", "Me", "Je", "Ve", "Sa"],
            monthNames: [
                "janvier",
                "Fevrier",
                "Mars",
                "Avril",
                "Mai",
                "Juin",
                "Juillet",
                "Aout",
                "Septembre",
                "Octobre",
                "Novembre",
                "Decembre",
            ],
            firstDay: 1,
        },
    });

    // Buton appliquer les filtres
    $("#filtre-btn").click(function (e) {
        // recuperation des Id_CPT
        var Id_CPT = $(".select2-selection__choice").map(function () {
            return this.title;
        });

        Id_CPT = toArray(Id_CPT);

        if (Id_CPT.length == 0) {
            //
            return;
        }

        var startDate = $("#picker")
            .data("daterangepicker")
            .startDate.format("DD-MM-YYYY");
        var endDate = $("#picker")
            .data("daterangepicker")
            .endDate.format("DD-MM-YYYY");

        $.ajax({
            url: "/applyFiltre",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                value: Id_CPT,
                startDate: startDate,
                endDate: endDate,
            }),
            success: function (result, statut) {
                alert("Hello");
                // Plotly.newPlot("plot", result["plot"]);
                Plotly.plot("plot", result["plot"], {});
            },
            error: function (result) {
                alert("ERROR");
            },
            complete: function () {
                // alert("ET LA ?");
            },
        });
    });
});
