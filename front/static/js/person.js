var localhost = "http://127.0.0.1:8000";


function Person() {
}

//监听头像上传
Person.prototype.ListenAvatarBtnEvent = function () {
    avatarBtn = $('#avatar-btn');
    avatarBtn.change(function () {
        var file = avatarBtn[0].files[0];//取第0个按钮，file[0]取出第0个文件
        var formData = new FormData();
        formData.append('file', file);//将文件添加到formData中
        $.ajax({
            url: '/avatar/',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formData,
            success: function (result) {
                url = localhost + JSON.parse(result).url;
                $("#avatar").attr("src", url);
            }
        })
    });
};


// 改邮箱
Person.prototype.ListenChangeEmailEvent = function () {
    var changeBtn = $('.changeEmail');
    var emailInput = $("#id_email");
    changeBtn.click(function () {
        email = emailInput.val();
        Swal.fire({
            title: '修改邮箱',
            html:
                '<input id="swal-input1" placeholder="邮箱" value="' + email + '" class="swal2-input">',
            showCancelButton: true,
            cancelButtonText: "取消"
        }).then(function (isConfirm) {
            if (isConfirm.value) {
                newEmail = $('#swal-input1').val();
                $.ajax({
                    url: '/change_email/',
                    type: 'POST',
                    data: {
                        'email': newEmail
                    },
                    success: function (result) {
                        if (result.code ===200){
                             Swal.fire(
                                '修改成功!',
                                'success'
                            );
                            emailInput.attr('value',newEmail);
                        }else{
                            var emailError = "";
                            if (result.message.email){
                                emailError = result.message.email[0];
                            }else if(result.message.__all__){
                                emailError = result.message.__all__[0];
                            }else {
                                emailError =    result
                            }

                             Swal.fire(
                                 '修改失败!',
                                 emailError,
                                 'error'
                            )
                        }

                    }
                })
            }

        })
    })

};

//改用户名
Person.prototype.ListenChangeUsernameEvent = function () {
    var changeBtn = $('.changeUsername');
    var usernameInput = $("#id_username");
    changeBtn.click(function () {
        username = usernameInput.val();
        Swal.fire({
            title: '修改用户名',
            html:
                '<input id="swal-input2" placeholder="用户名" value="' + username + '" class="swal2-input">',
            showCancelButton: true,
            cancelButtonText: "取消"
        }).then(function (isConfirm) {
            if (isConfirm.value) {
                newUsername = $('#swal-input2').val();
                $.ajax({
                    url: '/change_username/',
                    type: 'POST',
                    data: {
                        'username': newUsername
                    },
                    success: function (result) {
                        if (result.code ===200){
                             Swal.fire(
                                '修改成功!',
                                'success'
                            );
                            usernameInput.attr('value',newUsername)
                        }else{
                            console.log(result);
                             Swal.fire(
                                 '修改失败!',
                                 '用户名已经存在!',
                                 'error'
                            )
                        }

                    }
                })
            }

        })
    })

};






Person.prototype.run = function () {
    this.ListenAvatarBtnEvent();
    this.ListenChangeEmailEvent();
    this.ListenChangeUsernameEvent();
};


$(function () {
    var person = new Person();
    person.run();
});
