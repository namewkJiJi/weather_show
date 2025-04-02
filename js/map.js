// document.addEventListener("DOMContentLoaded", function() {
//     // 初始化地图，设置视角到中国
//     var map = L.map('map').setView([35.86166, 104.195397], 4);
//
//     // 使用空白图层，仅显示GeoJSON内容
//     L.tileLayer('', {
//         attribution: '',
//     }).addTo(map);
//
//     // 加载JSON文件，显示中国各省边界
//     fetch('static/src/pro_line.json')//flask中，路径不是以当前文件开始的，而是以很目录为开始
//         .then(response => response.json())
//         .then(data => {
//             // 创建GeoJSON图层，并添加交互功能
//             L.geoJSON(data, {
//                 style: function (feature) {
//                     return {
//                         color: "#3388ff", // 边界线颜色
//                         weight: 2,        // 边界线宽度
//                         fillOpacity: 0 // 默认不填充
//                     };
//                 },
//                 onEachFeature: function (feature, layer) {
//                     // 发送请求获取天气信息
//                     fetch(`/weather/${feature.properties.center}`)
//                         .then(response => response.json())
//                         .then(weather => {
//                             var tooltipContent = `
//                                 <strong>${feature.properties.name}</strong><br>
//                                 天气：${weather.text}<br>
//                                 温度：${weather.temp}℃<br>
//                                 过去1小时降水量：${weather.precip} mm<br>
//                                 风向：${weather.windDir} `;
//
//                             layer.bindTooltip(tooltipContent, {
//                                 permanent: false,
//                                 direction: 'top',
//                                 offset: [0, 10],
//                                 className: 'custom-tooltip'
//                             });
//                         });
//
//                     // 鼠标悬停时突出显示
//                     layer.on('mouseover', function () {
//                         this.setStyle({
//                             color: "#ff7800", // 悬停时边界线颜色
//                             weight: 4,        // 悬停时边界线宽度
//                             fillColor: "#ffcc00", // 悬停时填充颜色
//                             fillOpacity: 0.5  // 填充透明度
//                         });
//                         this.openTooltip(); // 显示标签
//                     });
//
//                     // 鼠标移出时恢复原样
//                     layer.on('mouseout', function () {
//                         this.setStyle({
//                             color: "#3388ff", // 恢复原样的边界线颜色
//                             weight: 2,        // 恢复原样的边界线宽度
//                             fillOpacity: 0 // 不填充
//                         });
//                         this.closeTooltip(); // 隐藏标签
//                     });
//
//                     // 点击时跳转到相应页面
//                     layer.on('click', function () {
//                         var provinceName = feature.properties.name; // 假设GeoJSON数据中有省份名称字段
//                         window.location.href = `/province/${provinceName}.html`; // 跳转到相应页面
//                     });
//                 }
//             }).addTo(map);
//
//         });
//     /* test */
//
//
// });


document.addEventListener("DOMContentLoaded", function() {
    // 初始化地图，设置视角到中国
    var map = L.map('map').setView([35.86166, 104.195397], 4);

    // 使用空白图层，仅显示GeoJSON内容
    L.tileLayer('', {
        attribution: '',
    }).addTo(map);

    // 颜色映射函数，根据温度返回不同颜色
    function getColor(temp) {
        return temp > 35 ? '#800026' :
               temp > 30 ? '#BD0026' :
               temp > 25 ? '#E31A1C' :
               temp > 20 ? '#FC4E2A' :
               temp > 15 ? '#FD8D3C' :
               temp > 10 ? '#FEB24C' :
               temp > 5  ? '#FED976' :
                           '#FFEDA0';
    }

    // 加载JSON文件，显示中国各省边界
    fetch('static/src/pro_line.json')
        .then(response => response.json())
        .then(data => {
            L.geoJSON(data, {
                style: function (feature) {
                    // 默认样式
                    return {
                        color: "#3388ff", // 边界线颜色
                        weight: 2,        // 边界线宽度
                        fillOpacity: 0.7  // 填充透明度
                    };
                },
                onEachFeature: function (feature, layer) {
                    // 发送请求获取天气信息
                    fetch(`/weather/${feature.properties.center}`)
                        .then(response => response.json())
                        .then(weather => {
                            var temp = weather.temp;
                            // 设置省份的填充颜色
                            layer.setStyle({
                                fillColor: getColor(temp),
                            });

                            var tooltipContent = `
                                <strong>${feature.properties.name}</strong><br>
                                天气：${weather.text}<br>
                                温度：${temp}℃<br>
                                风向：${weather.windDir}`;

                            layer.bindTooltip(tooltipContent, {
                                permanent: false,
                                direction: 'top',
                                offset: [0, 10],
                                className: 'custom-tooltip'
                            });

                        }).catch(() => {
                            // 如果请求失败，可以设置默认提示
                            layer.bindTooltip("天气信息加载失败", {
                                permanent: false,
                                direction: 'top',
                                offset: [0, 10],
                                className: 'custom-tooltip'
                            });
                        });

                    // 鼠标悬停时突出显示
                    layer.on('mouseover', function () {
                        this.setStyle({
                            color: "#ff7800", // 悬停时边界线颜色
                            weight: 4,        // 悬停时边界线宽度
                            fillOpacity: 0.9  // 填充透明度增加
                        });
                        this.openTooltip(); // 显示标签
                    });

                    // 鼠标移出时恢复原样
                    layer.on('mouseout', function () {
                        this.setStyle({
                            color: "#3388ff", // 恢复原样的边界线颜色
                            weight: 2,        // 恢复原样的边界线宽度
                            fillOpacity: 0.7  // 填充透明度恢复
                        });
                        this.closeTooltip(); // 隐藏标签
                    });

                    // 点击时跳转到相应页面
                    layer.on('click', function () {
                        var adcode = feature.properties.adcode; // 假设GeoJSON数据中有adcode字段
                        window.location.href = `/weather_detail?adcode=${adcode}`; // 使用URL参数传递adcode
                    });
                }
            }).addTo(map);

            // 添加图例到地图左下角
            var legend = L.control({position: 'bottomleft'});

            legend.onAdd = function (map) {
                var div = L.DomUtil.create('div', 'info legend'),
                    grades = [0, 5, 10, 15, 20, 25, 30, 35],
                    labels = [];

                // 循环生成图例内容
                for (var i = 0; i < grades.length; i++) {
                    div.innerHTML +=
                        '<div style="display: flex; align-items: center; margin-bottom: 5px;">' +
                        '<i style="width: 18px; height: 18px; background:' + getColor(grades[i] + 1) + '; margin-right: 8px;"></i>' +
                        grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '℃' : '+℃') +
                        '</div>';
                }

                return div;
            };

            legend.addTo(map);
        });
});
