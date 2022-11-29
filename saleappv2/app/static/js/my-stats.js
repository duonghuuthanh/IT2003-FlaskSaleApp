function cateChart(labels, data) {
    const ctx = document.getElementById('cateStats');

    new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Số lượng',
        data: data,
        borderWidth: 1,
        backgroundColor: ['red', 'green', 'blue', 'gold', 'brown', 'orange']
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function revenueChart(labels, data) {
    const ctx = document.getElementById('revenueStats');

    new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Doanh thu',
        data: data,
        borderWidth: 1,
        backgroundColor: ['red', 'green', 'blue', 'gold', 'brown', 'orange']
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}