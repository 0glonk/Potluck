document.addEventListener('DOMContentLoaded', function () {
    // Add event listeners to all logout links
    const logoutLinks = document.querySelectorAll(".logoutLink");
    logoutLinks.forEach(link => link.addEventListener("click", handleLogout));

    // Add event listeners to all bookmark buttons
    const bookmarkButtons = document.querySelectorAll(".bookmarkButton");
    bookmarkButtons.forEach(button => button.addEventListener("click", handleBookmarkToggle));

    const navbarCollapse = document.getElementById("navbarSupportedContent");

    // Toggles the ability of the body to scroll when the navbar is open
    navbarCollapse.addEventListener("show.bs.collapse", function () {
        document.body.classList.add("no-scroll");
    });
    navbarCollapse.addEventListener("hide.bs.collapse", function () {
        document.body.classList.remove("no-scroll");
    });

    const backdrop = document.getElementById("nav-backdrop");
    const navbar = document.querySelector(".navbar");

    // Adjusts the position of the backdrop to be below the navbar
    function updateBackdropPosition() {
        requestAnimationFrame(() => {
          setTimeout(() => {
            const navbarHeight = navbar.offsetHeight;
            backdrop.style.top = navbarHeight + "px";
            backdrop.style.height = `calc(100vh - ${navbarHeight}px)`;
          }, 50); // 50ms lets layout stabilize
        });
      }

    // Toggles the backdrop when the navbar is extended
    navbarCollapse.addEventListener("show.bs.collapse", function () {
        updateBackdropPosition();
        backdrop.style.display = "block";
        document.body.classList.add("no-scroll");
    });
    navbarCollapse.addEventListener("hide.bs.collapse", function () {
        backdrop.style.display = "none";
        document.body.classList.remove("no-scroll");
    });

    // Allows users to click outside the navbar to close it
    backdrop.addEventListener("click", function () {
        const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
        if (bsCollapse) bsCollapse.hide();
    });

    let resizeTimeout;
    // Recalculates backdrop position on window resizeq
    window.addEventListener("resize", function () {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            updateBackdropPosition();

            if (window.innerWidth >= 992) {
                const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                if (bsCollapse && navbarCollapse.classList.contains("show")) {
                    bsCollapse.hide();
                }
            }
        }, 100);
    });
});

/* Handles logout function for all logout links */
function handleLogout(event) {
    event.preventDefault();

    if (confirm("Are you sure you want to log out?")) {
        document.getElementById('logout-form').submit();
    }
}

/* Obsolete due to new interaction.js function

function handleBookmarkToggle(event) {
    fetch(`/toggle-bookmark`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        },
        //This needs to be updated to include the relevant id
        //body: JSON.stringify({ item_id: postId })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Update the UI based on the response
        })
        .catch(error => console.error('Error:', error));
} */