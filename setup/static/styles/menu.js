document.addEventListener('DOMContentLoaded', function() {
    var menuItem = document.querySelectorAll('.item-menu');
    var currentPage = window.location.pathname;

    function markActiveMenu() {
        menuItem.forEach((item) => {
            var link = item.querySelector('a');
            if (link.getAttribute('href') === currentPage) {
                item.classList.add('ativo');
            }
        });
    }

    markActiveMenu();

    var btnExp = document.querySelector('#btn-exp');
    var menuSide = document.querySelector('.menu-lateral');
    var pagina = document.querySelector('.pagina');

    btnExp.addEventListener('click', function() {
        menuSide.classList.toggle('expandir');
        if (menuSide.classList.contains('expandir')) {
            pagina.style.marginLeft = '190px';
        } else {
            pagina.style.marginLeft = '100px';
        }
    });
});