function submitPost(event) {
    event.preventDefault();

    var input = document.getElementById('username').value;

    var regex = /^1[3456789]\d{9}$/;

    if (!regex.test(input)) {
        alert("手机号格式错误!");
        location.reload();
    }

    var formData = new FormData(this);

    var password = formData.get('password')
    var hashedPassword = CryptoJS.MD5(password).toString()

    formData.set("password", hashedPassword)

    var jsonData = {};
    formData.forEach(function (value, key) {
        jsonData[key] = value;
    });
    jsonData = JSON.stringify(jsonData);

    // 发送POST请求
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:8000/login", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // 请求成功处理
            console.log(xhr.responseText);
            alert('登陆成功!');
            window.location.href = './index.html';
        } else if (xhr.readyState === 4) {
            if (xhr.status === 401) {
                alert('账号或密码错误，请重新输入。');
                location.reload();
            } else {
                alert("请求失败：" + xhr.status);
                location.reload();
            }
        }
    };
    xhr.send(jsonData);

}

document.getElementById("loginForm").addEventListener("submit", submitPost);