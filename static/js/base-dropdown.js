const dropdown = document.getElementById("accommodationDropdown");
let timeoutId;

function showDropdown() {
    timeoutId = setTimeout(() => {
        dropdown.style.display = "block";
    }, 500);
}

function hideDropdown() {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
        dropdown.style.display = "none";
    }, 500);
}

dropdown.parentNode.addEventListener("mouseenter", showDropdown);
dropdown.parentNode.addEventListener("mouseleave", hideDropdown);