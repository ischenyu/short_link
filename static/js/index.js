$(document).ready(function() {
            $('#addform').on('submit', function(event) {
                event.preventDefault(); // 阻止表单默认提交

                // 使用 serializeJSON 将表单数据序列化为 JSON
                const data = $(this).serializeJSON();

                // 发送数据到后端
                $.ajax({
                    type: 'POST',
                    url: '/api/user/new', // 替换为你的后端URL
                    data: JSON.stringify(data),
                    contentType: 'application/json',
                    success: function(response) {
                        $('#response-message').html(`<div class="alert alert-success" style="color: #000000">短链接生成成功: ${response.shortened_url}</div>`);
                    },
                    error: function(error) {
                        $('#response-message').html(`<div class="alert alert-danger" style="color: #000000">提交失败`);
                    }
                });
            });
        });