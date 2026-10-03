document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".nav-button");

    const appSection = document.querySelector(".app-buttons");
    const appButtons = document.querySelectorAll(".app-button");

    const helpSection = document.getElementById("help-content");
    const comingSoonSection = document.getElementById("coming-soon-content");

    function hide(element) {
        element.classList.add("is-hidden");
    }

    function show(element) {
        element.classList.remove("is-hidden");
    }

    function changePage(page) {
        // Hide all main content sections first
        hide(appSection);
        hide(helpSection);
        hide(comingSoonSection);

        // Hide all application buttons first
        appButtons.forEach(function (button) {
            hide(button);
        });

        // Home page: show every application button
        if (page === "home") {
            show(appSection);

            appButtons.forEach(function (button) {
                show(button);
            });
        }

        // Games page: show only game buttons
        else if (page === "games") {
            show(appSection);

            appButtons.forEach(function (button) {
                const category = button.getAttribute("data-category");

                if (category === "game") {
                    show(button);
                }
            });
        }

        // Tools page: show only tool buttons
        else if (page === "tools") {
            show(appSection);

            appButtons.forEach(function (button) {
                const category = button.getAttribute("data-category");

                if (category === "tool") {
                    show(button);
                }
            });
        }

        // Coming Soon page: show only Coming Soon content
        else if (page === "coming-soon") {
            show(comingSoonSection);
        }

        // Help page: show only Help content
        else if (page === "help") {
            show(helpSection);
        }

        // Update the active navigation link
        navLinks.forEach(function (link) {
            const linkPage = link.getAttribute("href").replace("#", "");

            if (linkPage === page) {
                link.classList.add("active");
            } else {
                link.classList.remove("active");
            }
        });
    }

    // Make each navigation link change the page
    navLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();

            const page = link.getAttribute("href").replace("#", "");

            changePage(page);
        });
    });

    // Start on the Home page and show all application buttons
    changePage("home");
});
