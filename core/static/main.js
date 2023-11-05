document.addEventListener('DOMContentLoaded', (event) => {
    let currentPath = window.location.pathname;

    let navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    navLinks.forEach((link) => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});
