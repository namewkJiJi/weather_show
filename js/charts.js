let lineChartInstance, pieChartInstance, barChartInstance;

document.addEventListener("DOMContentLoaded", function() {
    // 获取上下文
    const lineCtx = document.getElementById('lineChart').getContext('2d');
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    const barCtx = document.getElementById('barChart').getContext('2d');

    // 初始化图表，无数据
    lineChartInstance = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: [], // 空标签
            datasets: [{
                label: '气温曲线图 (℃)',
                data: [], // 空数据
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    pieChartInstance = new Chart(pieCtx, {
        type: 'doughnut',
        data: {
            labels: [], // 空标签
            datasets: [{
                label: '天气情况',
                data: [], // 空数据
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)'
                ],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                }
            }
        }
    });

    barChartInstance = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: [], // 空标签
            datasets: [{
                label: '空气质量',
                data: [], // 空数据
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    console.log('year= ',year)
     // 使用默认省市值请求并显示初始图表数据
    fetchChartDataAndUpdate('/chart-data', {
        province: defaultProvince,
        city: defaultCity,
        year: year
    });

    // 监听城市选择变化
    document.getElementById('city').addEventListener('change', function() {
        const city = this.value;

        // 根据选择的城市获取更新后的数据
        fetchChartDataAndUpdate('/chart-data', { city: city });
    });
});

function fetchChartDataAndUpdate(url, postData = {}) {
    const fetchOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    };

    fetch(url, fetchOptions)
        .then(response => response.json())
        .then(data => {
            updateCharts(data);
        })
        .catch(error => console.error('Error:', error));
}

function updateCharts(data) {
    // 更新折线图
    lineChartInstance.data.labels = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
    lineChartInstance.data.datasets[0].data = data.line;
    lineChartInstance.update();

    // 更新环形图
    pieChartInstance.data.labels = data.pie_tip;
    pieChartInstance.data.datasets[0].data = data.pie;
    pieChartInstance.update();

    // 更新柱状图
    barChartInstance.data.labels = ['优','良','轻度污染','中度污染','重度污染','严重污染'];
    barChartInstance.data.datasets[0].data = data.aqi;
    barChartInstance.update();
}
