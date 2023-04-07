// Function to change webpage background color
function changeBodyBg(color) {
}

window.onload = function () {
    document.getElementById("color_picker").addEventListener("change", watchColorPicker, false);
    document.getElementById("color_picker").addEventListener("input", watchColorPicker, false);

};

function watchColorPicker(event) {
    document.getElementById("results_background").style.backgroundColor = event.target.value;

}
