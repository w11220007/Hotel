document.querySelector('.search-input').addEventListener('input', function() {
    const input = this.value.trim().toLowerCase().replace(/\s/g, '');
    const dropdownItems = document.querySelectorAll('.destination .dropdown-menu li');

    let cityExists = false;
    dropdownItems.forEach(item => {
        const city = item.dataset.city.toLowerCase().replace(/\s/g, '');
        if (city === input) {
            cityExists = true;
        }
    });

    dropdownItems.forEach(item => {
        const city = item.dataset.city.toLowerCase().replace(/\s/g, '');
        if (city.includes(input)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
});

document.querySelector(".destination .search-btn").addEventListener("click", function() {
    const selectedCity = document.querySelector(".destination .search-input").value.trim().toLowerCase().replace(/\s/g, "");
    const dropdownItems = document.querySelectorAll(".destination .dropdown-menu li");
    let cityExists = false;

    dropdownItems.forEach(item => {
        if (item.dataset.city.toLowerCase().replace(/\s/g, "") === selectedCity) {
            cityExists = true;
        }
    });

    if (selectedCity != "" && !cityExists) {
        alert("The destination you selected does not exist.");
    } else {
        if (selectedCity === "") {
            alert("Please select a destination");
        } else {
            window.location.href = `/searchbydestination/${selectedCity}`;
        }
    }
});

document.querySelector(".destination .search-input").addEventListener("focus", function() {
    document.querySelector(".destination .dropdown-menu").style.display = "block";
});

document.querySelectorAll(".destination .dropdown-menu li").forEach(item => {
    item.addEventListener("click", function() {
        document.querySelector(".destination .search-input").value = this.dataset.city;
        document.querySelector(".destination .dropdown-menu").style.display = "none";
    });
});


