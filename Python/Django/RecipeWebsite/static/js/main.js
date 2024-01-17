// static/js/main.js

document.addEventListener("DOMContentLoaded", function () {
    console.log("main.js worked!");
    const countryForm = document.getElementById("countryForm");
    const mealForm = document.getElementById("mealForm");

    countryForm.addEventListener("change", function () {
        this.submit();
    });

    mealForm.addEventListener("change", function () {
        this.submit();
    });
});

