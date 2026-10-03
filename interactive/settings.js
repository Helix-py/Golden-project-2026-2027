document.addEventListener("DOMContentLoaded", function () {
    const navigationLinks = document.querySelectorAll(
        ".settings-sidebar nav a"
    );

    const settingsSections = document.querySelectorAll(
        ".settings-section"
    );

    navigationLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();

            const sectionId = link
                .getAttribute("href")
                .replace("#", "");

            settingsSections.forEach(function (section) {
                section.classList.remove("active");
            });

            navigationLinks.forEach(function (navigationLink) {
                navigationLink.classList.remove("active");
            });

            const selectedSection = document.getElementById(sectionId);

            if (selectedSection) {
                selectedSection.classList.add("active");
                link.classList.add("active");
            }
        });
    });
});
