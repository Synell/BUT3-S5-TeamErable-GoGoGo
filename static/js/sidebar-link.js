document.querySelectorAll(".sidebar-link, .navbar-link").forEach(function (element) {
  element.addEventListener('click', function (event) {
    var links = document.querySelectorAll(".sidebar-link, .navbar-link");
    links.forEach(element => {
      element.classList.remove("active");
    });

    var sections = document.querySelectorAll("section");
    sections.forEach(element => {
      element.classList.remove("active");
    });

    event.target.classList.toggle("active");
    document.querySelector(event.target.getAttribute("activate")).classList.toggle("active");
  });
});
