document.querySelector('.menu-toggle').addEventListener('click', function(){
    document.querySelector('.nav').classList.toggle('mobile-nav');
    this.classList.toggle('is-active');
});

/**
 * Fonction pour afficher le menu de profil
 */
function pfpMenuToggle() {
    const toggleMenu = document.querySelector(".pfp-menu");
    toggleMenu.classList.toggle("active");
}
