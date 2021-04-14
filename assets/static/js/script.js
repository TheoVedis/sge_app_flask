function openNav() {
    /* Documentation
    Cette fonction a pour but d'ouvrir et fermer le menu lattéral
    ainsi que décaler le contenu de la page principal vers la droite

    Parametre:
        val: nombre de click qu'un utilisateur a effectué sur le bouton
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
