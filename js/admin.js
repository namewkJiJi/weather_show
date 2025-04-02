function openAddDataModal() {
    console.log("Opening Add Data Modal");
    document.getElementById('dataModel').style.display = 'block';
    document.getElementById('dataForm').action = '/admin/add_data'; // 对应添加数据的路由
}

        function openUpdateDateModal() {
            document.getElementById('dataModel').style.display = 'block';
            document.getElementById('dataForm').action = '/admin/update_data'; // 对应修改数据的路由
        }

function deleteData() {
    console.log("Opening delete Data Modal");
    var id = prompt("请输入要删除的id:");
    if (id) {
        window.location.href = "/admin/delete_data?id=" + id; // 对应删除数据的路由
    }
}

function addData() {
    var id = prompt("请输入id:");
    var temp = prompt("请输入温度:");
    var aireaq = prompt("请输入空气质量:");
    var dy = prompt("请输入多云情况:");
    var qing = prompt("请输入晴情况:");
    var hc = prompt("请输入沙尘情况:");
    var xue = prompt("请输入雪情况:");
    var yu = prompt("请输入雨情况:");
    var yin = prompt("请输入阴情况:");
    var city = prompt("请输入城市:");
    var month = prompt("请输入月份:");
    var year = prompt("请输入年份:");

    // 打印所有字段值进行调试
    console.log('id:', id);
    console.log('temp:', temp);
    console.log('aireaq:', aireaq);
    console.log('dy:', dy);
    console.log('qing:', qing);
    console.log('hc:', hc);
    console.log('xue:', xue);
    console.log('yu:', yu);
    console.log('yin:', yin);
    console.log('city:', city);
    console.log('month:', month);
    console.log('year:', year);

    // 判断所有输入是否都已填写
    if (id && temp && aireaq && dy && qing && hc && xue && yu && yin && city && month && year) {
        // 使用 fetch 发送 POST 请求到 Flask 后端
        fetch('/admin/add_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: id,
                temp: temp,
                aireaq: aireaq,
                dy: dy,
                qing: qing,
                hc: hc,
                xue: xue,
                yu: yu,
                yin: yin,
                city: city,
                month: month,
                year: year
            })
        }).then(response => {
            if (response.ok) {
                alert('数据添加成功');
                window.location.reload();  // 刷新页面以显示新数据
            } else {
                alert('添加失败，请重试');
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('添加失败，请检查网络连接');
        });
    } else {
        alert("所有字段都是必填的");
    }
}

function updateData() {
    // 1. 获取要修改的 id
    var id = prompt("请输入要修改的id:");

    if (id) {
        // 2. 选择要修改的字段
        var field = prompt("请选择要修改的字段：\n1. 温度\n2. 空气质量\n3. 多云\n4. 晴\n5. 沙尘\n6. 雪\n7. 雨\n8. 阴");

        // 3. 根据选择的字段弹出输入框
        var newValue = "";
        switch (field) {
            case '1':
                newValue = prompt("请输入新的温度:");
                field = "temp";  // 设置字段为 "temp"
                break;
            case '2':
                newValue = prompt("请输入新的空气质量:");
                field = "aireaq";  // 设置字段为 "aireaq"
                break;
            case '3':
                newValue = prompt("请输入新的多云情况:");
                field = "dy";  // 设置字段为 "dy"
                break;
            case '4':
                newValue = prompt("请输入新的晴情况:");
                field = "qing";  // 设置字段为 "qing"
                break;
            case '5':
                newValue = prompt("请输入新的沙尘情况:");
                field = "hc";  // 设置字段为 "hc"
                break;
            case '6':
                newValue = prompt("请输入新的雪情况:");
                field = "xue";  // 设置字段为 "xue"
                break;
            case '7':
                newValue = prompt("请输入新的雨情况:");
                field = "yu";  // 设置字段为 "yu"
                break;
            case '8':
                newValue = prompt("请输入新的阴情况:");
                field = "yin";  // 设置字段为 "yin"
                break;
            default:
                alert("无效选择");
                return;
        }

        // 4. 判断是否输入了新值
        if (newValue.trim() !== "") {
            // 发送 POST 请求到 Flask 后端
            fetch('/admin/update_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: id.trim(),
                    field: field,
                    newValue: newValue.trim()
                })
            }).then(response => {
                if (response.ok) {
                    alert('数据修改成功');
                    window.location.reload();  // 刷新页面以显示修改后的数据
                } else {
                    alert('修改失败，请重试');
                }
            }).catch(error => {
                console.error('Error:', error);
                alert('修改失败，请检查网络连接');
            });
        } else {
            alert("请输入有效的值");
        }
    } else {
        alert("请输入有效的id");
    }
}



function openModal() {
    document.getElementById('dataModel').style.display = 'block';
    document.getElementById('modalOverlay').style.display = 'block';
}

function closeModal() {
    document.getElementById('dataModel').style.display = 'none';
    document.getElementById('modalOverlay').style.display = 'none';
}

