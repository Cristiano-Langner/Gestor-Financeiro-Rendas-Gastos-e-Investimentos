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
            pagina.style.marginLeft = '300px';
            localStorage.setItem('menuExpanded', 'true');
        } else {
            pagina.style.marginLeft = '140px';
            localStorage.setItem('menuExpanded', 'false');
        }
    });

    var isMenuExpanded = localStorage.getItem('menuExpanded');
    console.log('Estado do menu:', isMenuExpanded);
    if (isMenuExpanded === 'true') {
        menuSide.classList.add('expandir');
        pagina.style.marginLeft = '300px';
    }
});