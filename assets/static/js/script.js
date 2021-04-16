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
                var plot = [
                    {
                        x: [
                            1222820000000.0,
                            1222840000000.0,
                            1222850000000.0,
                            1222870000000.0,
                            1222880000000.0,
                            1222900000000.0,
                            1222820000000.0,
                            1222830000000.0,
                            1222850000000.0,
                            1222860000000.0,
                            1222880000000.0,
                            1222890000000.0,
                            1222820000000.0,
                            1222830000000.0,
                            1222840000000.0,
                            1222860000000.0,
                            1222870000000.0,
                            1222890000000.0,
                            1222810000000.0,
                            1222830000000.0,
                            1222840000000.0,
                            1222860000000.0,
                            1222870000000.0,
                            1222880000000.0,
                        ],
                        y: [
                            1096808.0,
                            1096827.0,
                            1097029.0,
                            1097217.0,
                            1097438.0,
                            1097632.0,
                            1096804.0,
                            1096821.0,
                            1096971.0,
                            1097169.0,
                            1097373.0,
                            1097597.0,
                            1096796.0,
                            1096816.0,
                            1096909.0,
                            1097127.0,
                            1097317.0,
                            1097555.0,
                            1096785.0,
                            1096812.0,
                            1096851.0,
                            1097084.0,
                            1097265.0,
                            1097504.0,
                        ],
                        type: "scatter",
                    },
                ];
                // Plotly.newPlot("plot", plot);
                Plotly.newPlot("plot", result["plot"]);
                // Plotly.plot("plot", plot, {});
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
