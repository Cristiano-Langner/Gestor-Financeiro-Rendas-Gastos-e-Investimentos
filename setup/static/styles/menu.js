document.addEventListener('DOMContentLoaded', function() {
    var menuItem = document.querySelectorAll('.item-menu');
    var currentPage = window.location.pathname;

    function getSecondElementFromPath(path) {
        var pathParts = path.split('/');
        return pathParts.length > 2 ? pathParts[2] : null;
    }

    function markActiveMenu() {
        menuItem.forEach((item) => {
            var link = item.querySelector('a');
            var currentSecondElement = getSecondElementFromPath(currentPage);
            if (link.getAttribute('href') === currentPage || link.getAttribute('href') === '/' + currentSecondElement) {
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