function drawCrates() {
    console.log('huj')


    for (i = 0; i < 10; i++) {
        var crate_img = document.createElement("IMG");
        crate_img.setAttribute("src", "../AlbumCovers/1.jpg");
        crate_img.classList.add("box")
        document.getElementById("Mosaic").appendChild(crate_img);


    }
}


window.addEventListener("load", () => {
  function sendData() {
    const XHR = new XMLHttpRequest();

    // Bind the FormData object and the form element
    const FD = new FormData(form);

    // Define what happens on successful data submission
    XHR.addEventListener("load", (event) => {
      alert(event.target.responseText);
    });

    // Define what happens in case of error
    XHR.addEventListener("error", (event) => {
      alert('Oops! Something went wrong.');
    });

    // Set up our request
    XHR.open("POST", "https://example.com/cors.php");

    // The data sent is what the user provided in the form
    XHR.send(FD);
  }

  // Get the form element
  const form = document.getElementById("myForm");

  // Add 'submit' event handler
  form.addEventListener("submit", (event) => {
    event.preventDefault();

    sendData();
  });
});

