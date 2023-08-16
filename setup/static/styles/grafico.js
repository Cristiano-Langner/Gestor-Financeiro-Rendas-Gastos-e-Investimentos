var chartOptions = {
    responsive: true,
    plugins: {
        legend: {
            display: false
        }
    }
};

var rendasChart = new Chart(document.getElementById('grafico-rendas').getContext('2d'), {
    type: 'pie',
    data: rendasData,
    options: chartOptions
});

var categoriasChart = new Chart(document.getElementById('grafico-categorias').getContext('2d'), {
    type: 'pie',
    data: categoriasData,
    options: chartOptions
});