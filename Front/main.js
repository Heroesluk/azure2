function drawCrates() {

    for (i = 0; i < 9; i++) {
        var crate_img = document.createElement("IMG");
        crate_img.setAttribute("src", "../AlbumCovers/1.jpg");
        crate_img.classList.add("box")
        document.getElementById("Mosaic").appendChild(crate_img);


    }
}

drawCrates();