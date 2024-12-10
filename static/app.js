document.addEventListener("DOMContentLoaded", () => {
    const loginButton = document.getElementById("login-button");
    const loginForm = document.getElementById("login-form");
    const wineOverlay = document.getElementById("wine-overlay");

    if (loginButton && loginForm && wineOverlay) {
        console.log("Elements found");

        loginButton.addEventListener("click", (event) => {
            event.preventDefault();  // Stop immediate form submission
            console.log("Login button clicked");

            // Trigger Animation
            wineOverlay.classList.add("animated");
            console.log("Animation triggered");

            // Submit the form after a delay (matching the animation time)
            setTimeout(() => {
                console.log("Form submitted after animation");
                loginForm.submit();  // Redirects after animation completes
            }, 6000);  // Delay for the animation duration (6 seconds)
        });
    } else {
        console.error("Required elements not found.");
    }
});
