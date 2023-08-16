var chartOptions = {
    responsive: true,
    plugins: {
        legend: {
            display: false
        }
    }
};

var gastosChart = new Chart(document.getElementById('grafico-gastos').getContext('2d'), {
    type: 'pie',
    data: gastosData,
    options: chartOptions,
});

var categoriasgastosChart = new Chart(document.getElementById('grafico-categorias-gastos').getContext('2d'), {
    type: 'pie',
    data: categoriasgastosData,
    options: chartOptions
});