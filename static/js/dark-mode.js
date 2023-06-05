// dark-mode.js
$(document).ready(function () {
    // get the html element
    const html = $("html");

    // get the dark mode switcher
    const switcher = $("#dark-mode-switch");

    // check if user has a preference
    const preference = localStorage.getItem("dark-mode");

    // if user has a preference, apply it
    if (preference) {
        html.attr("data-bs-theme", preference);
        // check or uncheck the switcher
        switcher.prop("checked", preference === "dark");
    }

    // listen for switcher change
    switcher.on("change", function () {
        // get the current theme
        let theme = html.attr("data-bs-theme");
        // toggle between light and dark
        theme = theme === "light" ? "dark" : "light";
        // apply the new theme
        html.attr("data-bs-theme", theme);
        // save the preference
        localStorage.setItem("dark-mode", theme);
    });
});
