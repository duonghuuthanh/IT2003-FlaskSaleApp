function cateChart(labels, data) {
  const ctx = document.getElementById('cateChart');

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Thống kê số sản phẩm theo danh mục',
        data: data,
        borderWidth: 1,
        backgroundColor: ['red', 'green', 'blue', 'gold', 'green', 'brown']
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
  const ctx = document.getElementById('revenueChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Thống kê doanh thu',
        data: data,
        borderWidth: 1,
        backgroundColor: ['red', 'green', 'blue', 'gold', 'brown']
      }],
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
