document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("themeToggle");
    const body = document.body;
    const footerText = document.querySelectorAll(".text-body-secondary");
    const headerText = document.querySelector(".fs-4");

    // Load saved theme from localStorage
    const savedTheme = localStorage.getItem("theme") || "light";
    body.setAttribute("data-theme", savedTheme);

    function applyTheme(theme) {
        if (theme === "dark") {
            footerText.forEach(text => text.style.color = "white");
            headerText.style.color = "white";
        } else {
            footerText.forEach(text => text.style.color = "black");
            headerText.style.color = "black";
        }
    }
    applyTheme(savedTheme);

    themeToggle.addEventListener("click", function () {
        let currentTheme = body.getAttribute("data-theme");
        let newTheme = currentTheme === "light" ? "dark" : "light";
        body.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        applyTheme(newTheme);
    });
});
