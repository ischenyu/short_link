
// 当get_button被点击
$('#get_button').on('click', function(event) {
    var email = $('#email').val();
    // 发送数据到后端
    $.ajax({
        type: 'POST',
        url: '/user/code', // 替换为你的后端URL
        data: JSON.stringify({"email": email}), // 确保data是JSON格式
        contentType: 'application/json',
        dataType: 'json', // 设置预期的响应类型
        success: function(response) {
            if (response.code === 200){
                $('#response-message').html(`<div class="alert alert-success" style="color: #000000">发送验证码成功</div>`);
            } else {
                $('#response-message').html(`<div class="alert alert-danger" style="color: #000000">发送验证码失败${response.msg}</div>`);
            }
        },
        error: function(xhr, status, error) {
            // 显示具体的错误信息
            var errorMessage = xhr.responseText || "提交失败";
            $('#response-message').html(`<div class="alert alert-danger" style="color: #000000">${errorMessage}</div>`);
        }
    });
});


$(document).ready(function() {
    $('.user_login').on('submit', function(event) {
        event.preventDefault(); // 阻止表单默认提交

        // 使用 serializeJSON 将表单数据序列化为 JSON
        const data = $(this).serializeJSON();

        // 发送数据到后端
        $.ajax({
            type: 'POST',
            url: '/user/login', // 替换为你的后端URL
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(response) {
                $('#response-message').html(`<div class="alert alert-success" style="color: #000000">短链接生成成功: ${response.shortened_url}</div>`);
            },
            error: function(error) {
                $('#response-message').html(`<div class="alert alert-danger" style="color: #000000">提交失败</div>`);
            }
        });
    });
});




