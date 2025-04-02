let rainfallChartInstance,forecastRow,day1Box;

document.addEventListener('DOMContentLoaded', function() {
    forecastRow = document.getElementById('forecast-row');
    day1Box = document.getElementById('day1-box');
    const rainfallCtx = document.getElementById('rainfallChart').getContext('2d');


    //初始化图表
    //  rainfallChartInstance = new Chart(rainfallCtx, {
    //                     type: 'line',
    //                     data: {
    //                         labels: [],
    //                         datasets: [
    //                          {
    //                             label: 'Max Temperature (°C)',
    //                             data: [],
    //                             backgroundColor: 'rgba(255, 99, 132, 0.2)',
    //                             borderColor: 'rgba(255, 99, 132, 1)',
    //                             borderWidth: 1
    //                         },
    //                         {
    //                             label: 'Min Temperature (°C)',
    //                             data: [],
    //                             backgroundColor: 'rgba(75, 192, 192, 0.2)',
    //                             borderColor: 'rgba(75, 192, 192, 1)',
    //                             borderWidth: 1
    //                         }]
    //                     },
    //                     options: {
    //                         responsive: true,
    //                         scales: {
    //                             y: {
    //                                 beginAtZero: true
    //                             }
    //                         }
    //                     }
    //                 });
    rainfallChartInstance = new Chart(rainfallCtx, {
    type: 'line',
    data: {
        labels: [],  // 图表的 X 轴标签
        datasets: [
            {
                label: 'Max Temperature (°C)',
                data: [],  // 最大气温数据
                backgroundColor: 'rgba(255, 99, 132, 0.2)', // 背景色
                borderColor: 'rgba(255, 99, 132, 1)', // 边框颜色
                borderWidth: 2, // 边框宽度
                pointBackgroundColor: 'rgba(255, 99, 132, 1)', // 数据点背景色
                pointBorderColor: '#fff', // 数据点边框色
                pointBorderWidth: 1, // 数据点边框宽度
                pointRadius: 5, // 数据点半径
            },
            {
                label: 'Min Temperature (°C)',
                data: [],  // 最低气温数据
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // 背景色
                borderColor: 'rgba(75, 192, 192, 1)', // 边框颜色
                borderWidth: 2, // 边框宽度
                pointBackgroundColor: 'rgba(75, 192, 192, 1)', // 数据点背景色
                pointBorderColor: '#fff', // 数据点边框色
                pointBorderWidth: 1, // 数据点边框宽度
                pointRadius: 5, // 数据点半径
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top', // 图例位置
                labels: {
                    font: {
                        size: 14 // 图例字体大小
                    },
                    color: '#333' // 图例字体颜色
                }
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        return `${tooltipItem.dataset.label}: ${tooltipItem.raw}°C`;
                    }
                },
                backgroundColor: 'rgba(0, 0, 0, 0.7)', // 工具提示背景色
                bodyFont: {
                    size: 14 // 工具提示字体大小
                },
                titleFont: {
                    size: 16 // 工具提示标题字体大小
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    font: {
                        size: 12 // X 轴字体大小
                    },
                    color: '#333' // X 轴字体颜色
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)', // X 轴网格线颜色
                    borderColor: 'rgba(0, 0, 0, 0.1)' // X 轴边框线颜色
                }
            },
            y: {
                beginAtZero: true,
                ticks: {
                    font: {
                        size: 12 // Y 轴字体大小
                    },
                    color: '#333' // Y 轴字体颜色
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)', // Y 轴网格线颜色
                    borderColor: 'rgba(0, 0, 0, 0.1)' // Y 轴边框线颜色
                }
            }
        }
    }
});


    // 初始加载天气数据
    fetchUpdateWeatherData('/weather-data',{
        province: defaultProvince,
        city: defaultCity
    });

    // 监听城市选择变化
    document.getElementById('city').addEventListener('change', function() {
        const city = this.value;

        // 根据选择的城市获取更新后的数据
        fetchUpdateWeatherData('/weather-data', { city: city });
    });
});


function fetchUpdateWeatherData(url, postData = {}) {
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
            updateWeatherData(data)
        })
        .catch(error => console.error('Error:', error));
}

function updateWeatherData(data){
    const labels = [];
    const tempMaxData = [];
    const tempMinData = [];

    // 清空之前的内容
    forecastRow.innerHTML = '';

    // 显示7天的数据
    data.forEach((day, index) => {
        labels.push(day.fxDate);
        tempMaxData.push(day.tempMax);
        tempMinData.push(day.tempMin);

        if (index === 0) {
            day1Box.style.width = '100%';

            day1Box.innerHTML =
              `
                <div style="display: flex; justify-content: space-between;">
                    <div style="flex: 1;">
                        <h2>${day.fxDate}</h2>
                        <p>最高气温: ${day.tempMax}°C</p>
                        <p>最低气温: ${day.tempMin}°C</p>
                        <p>能见度: ${day.vis}km</p>
                        <p>降水: ${day.precip}mm</p>
                    </div>
                    <div style="flex: 1; display: flex; justify-content: space-around;">
                        <div>
                            <p>白天天气: ${day.textDay}</p>
                            <img src="/static/src/icons/${day.iconDay}.svg" alt="${day.textDay}" style="width: 50px;">
                        </div>
                        <div>
                            <p>夜晚天气: ${day.textNight}</p>
                            <img src="/static/src/icons/${day.iconNight}.svg" alt="${day.textNight}" style="width: 50px;">
                        </div>
                        <div>
                            <p>月相: ${day.moonPhase}</p>
                            <img src="/static/src/icons/${day.moonPhaseIcon}.svg" alt="${day.moonPhase}" style="width: 50px;">
                        </div>
                    </div>
                </div>
            `
            ;
        } else {
            // 创建天气预报框
            const forecastBox = document.createElement('div');
            forecastBox.className = 'forecast-box';
            forecastBox.innerHTML = `
                <h2>${day.fxDate}</h2>
                <p>最高气温: ${day.tempMax}°C</p>
                <p>最低气温: ${day.tempMin}°C</p>
                <p>白天天气: ${day.textDay}</p>
                <p>夜晚天气: ${day.textNight}</p>
                <p>降水: ${day.precip}mm</p>
            `;
            forecastRow.appendChild(forecastBox);
        }
    });

    //更新折线图
    rainfallChartInstance.data.labels = labels;
    rainfallChartInstance.data.datasets[0].data = tempMaxData;
    rainfallChartInstance.data.datasets[1].data = tempMinData;
    rainfallChartInstance.update();
}
