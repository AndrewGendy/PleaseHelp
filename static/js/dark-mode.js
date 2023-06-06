// dark-mode.js
$(document).ready(function () {
    // Get the theme icon element
    const themeIcon = document.getElementById("theme-icon");

    // Get the theme dropdown element
    const themeDropdown = document.getElementById("theme-dropdown");

    // Get the light and dark option elements
    const lightOption = document.getElementById("light-option");
    const darkOption = document.getElementById("dark-option");

    // Get the current theme from the localStorage or default to light
    let currentTheme = localStorage.getItem("theme") || "light";

    // Get the option element that matches the current theme
    let currentOption = document.querySelector(`[data-bs-theme="${currentTheme}"] > div`);

    // Add the active class and the aria-pressed attribute to the current option
    currentOption.classList.add("active");
    currentOption.setAttribute("aria-pressed", "true");

    // Set the initial icon and dropdown menu according to the current theme
    if (currentTheme === "light") {
        // Set the icon to sun
        themeIcon.className = "fas fa-sun";
        // Remove this line: lightOption.classList.add("active");
        // Remove this line: lightOption.setAttribute("aria-pressed", "true");
    } else if (currentTheme === "dark") {
        // Set the icon to moon
        themeIcon.className = "fas fa-moon";
        // Remove this line: darkOption.classList.add("active");
        // Remove this line: darkOption.setAttribute("aria-pressed", "true");
    }

    // Change the html data-bs-theme attribute according to the current theme
    document.documentElement.setAttribute("data-bs-theme", currentTheme);

    // Add a click event listener to the light option
    lightOption.addEventListener("click", function () {
        // Change the html data-bs-theme attribute to light
        document.documentElement.setAttribute("data-bs-theme", "light");
        // Change the icon to sun
        themeIcon.className = "fas fa-sun";
        // Change the active and pressed option to light
        lightOption.classList.add("active");
        lightOption.setAttribute("aria-pressed", "true");
        darkOption.classList.remove("active");
        darkOption.setAttribute("aria-pressed", "false");
        // Save the theme value to localStorage
        localStorage.setItem("theme", "light");
    });

    // Add a click event listener to the dark option
    darkOption.addEventListener("click", function () {
        // Change the html data-bs-theme attribute to dark
        document.documentElement.setAttribute("data-bs-theme", "dark");
        // Change the icon to moon
        themeIcon.className = "fas fa-moon";
        // Change the active and pressed option to dark
        darkOption.classList.add("active");
        darkOption.setAttribute("aria-pressed", "true");
        lightOption.classList.remove("active");
        lightOption.setAttribute("aria-pressed", "false");
        // Save the theme value to localStorage
        localStorage.setItem("theme", "dark");
    });
});
