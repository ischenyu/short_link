
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


