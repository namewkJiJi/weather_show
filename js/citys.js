
document.addEventListener('DOMContentLoaded', function() {
    var provinceSelect = document.getElementById('province');
    var citySelect = document.getElementById('city');

    // Fetch the cities data from the Flask server
    fetch('/get_cities')
        .then(response => response.json())
        .then(data => {
            // Populate the province select box
            for (var province in data) {
                var option = document.createElement('option');
                option.value = province;
                option.textContent = province;
                provinceSelect.appendChild(option);
            }

            // 设置省的默认值
            provinceSelect.value = defaultProvince;

            // 更新城市下拉框为选中省的城市列表
            updateCities(defaultProvince, defaultCity);
        });

    provinceSelect.addEventListener('change', function() {
        updateCities(this.value);
    });

    function updateCities(province, selectedCity = null) {
        // 清空现有的城市选项并添加提示选项
        clearCitySelect();

        // 获取城市数据并更新城市下拉框
        fetch('/get_cities')
            .then(response => response.json())
            .then(data => {
                var cities = data[province];
                cities.forEach(function(city) {
                    var option = document.createElement('option');
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                });

                // 设置城市的默认值
                if (selectedCity) {
                    citySelect.value = selectedCity;
                }
            });
    }

    function clearCitySelect() {
        citySelect.innerHTML = '';

        // 添加一个提示用户选择城市的选项
        var defaultOption = document.createElement('option');
        defaultOption.selected = true;
        defaultOption.disabled = true;
        defaultOption.textContent = '请选择城市';
        citySelect.appendChild(defaultOption);
    }
});

