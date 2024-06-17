document.querySelector('.search-input').addEventListener('input', function() {
    const input = this.value.trim().toLowerCase().replace(/\s/g, '');
    const dropdownItems = document.querySelectorAll('.ranking .dropdown-menu li');

    let rankingExists = false;
    dropdownItems.forEach(item => {
        const ranking = item.dataset.ranking.toLowerCase().replace(/\s/g, '');
        if (ranking === input) {
            rankingExists = true;
        }
    });

    dropdownItems.forEach(item => {
        const ranking = item.dataset.ranking.toLowerCase().replace(/\s/g, '');
        if (ranking.includes(input)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
});

document.querySelector(".ranking .search-btn").addEventListener("click", function() {
    const selectedRanking = document.querySelector(".ranking .search-input").value.trim().toLowerCase().replace(/\s/g, "");
    const dropdownItems = document.querySelectorAll(".ranking .dropdown-menu li");
    let rankingExists = false;

    dropdownItems.forEach(item => {
        if (item.dataset.ranking.toLowerCase().replace(/\s/g, "") === selectedRanking) {
            rankingExists = true;
        }
    });

    if (selectedRanking != "" && !rankingExists) {
        alert("Ranking does not exist.");
    } else {
        if (selectedRanking === "") {
            alert("Please select ranking.");
        } else {
            window.location.href = `/searchbyranking/${selectedRanking}stars`;
        }
    }
});

document.querySelector(".ranking .search-input").addEventListener("focus", function() {
    document.querySelector(".ranking .dropdown-menu").style.display = "block";
});

document.querySelectorAll(".ranking .dropdown-menu li").forEach(item => {
    item.addEventListener("click", function() {
        document.querySelector(".ranking .search-input").value = this.dataset.ranking;
        document.querySelector(".ranking .dropdown-menu").style.display = "none";
    });
});


