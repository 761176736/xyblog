function Auth() {

}
//登陆
Auth.prototype.listenSigninEvent = function () {
    var self = this;
    var signinGroup = $('#signin-group');
    var emailInput = signinGroup.find("input[name='email']");//找到登陆电话对话框
    var passwordInput = signinGroup.find("input[name= 'password']");//密码对话框
    var rememberInput = signinGroup.find("input[name='remember']");

    var submitBtn = signinGroup.find('.submit-btn');
    var loginMessage = $('#login-errors');

    submitBtn.click(function () {
        var email = emailInput.val();
        var password = passwordInput.val();
        var remember = rememberInput.prop("checked");
        $.ajax({
            type: 'POST',
            url: '/log_page/login/',
            data: {
                'email': email,
                'password': password,
                'remember': remember ? 1 : 0
            },
            success: function (result) {
                if (result['code'] === 200){
                    location.href="../";
                }else{

                    console.log(result['message']);
                    if(result['message']['email']){
                        loginMessage.html(result['message']['email'][0]);
                        setTimeout(function () {
                            loginMessage.html('');
                        },2000);
                    }else {
                        loginMessage.html(result['message']);
                        setTimeout(function () {
                            loginMessage.html('');
                        },2000);
                    }
                }
            }
        })
    });
};

//注册
Auth.prototype.listenSignupEvent= function()
{
    var self = this;
    var signupGroup = $('#signup-group');
    var emailInput = signupGroup.find("input[name='email']");
    var usernameInput = signupGroup.find("input[name='username']");
    var pwd1Input = signupGroup.find("input[name='pwd1']");
    var pwd2Input = signupGroup.find("input[name='pwd2']");
    var submitBtn = signupGroup.find('.submit-btn');
    var message = $('#errors');


    submitBtn.click(function () {
        var email = emailInput.val();
        var username = usernameInput.val();
        var pwd1 = pwd1Input.val();
        var pwd2 = pwd2Input.val();
        $.ajax({
            type: 'POST',
            url: '/log_page/register/',
            data: {
                'email': email,
                'username': username,
                'pwd1':pwd1,
                'pwd2':pwd2
            },
            success: function (result) {
                if (result['code'] === 200){
                    location.href="../";
                }else{
                    if(result['message']['username']){
                        message.html(result['message']['username'][0]);
                        setTimeout(function () {
                            message.html('');
                        },2000);

                    }else if (result['message']['email']){
                        message.html(result['message']['email'][0]);
                         setTimeout(function () {
                            message.html('');
                        },2000);

                    }else if (result['message']['pwd1']){
                        message.html(result['message']['pwd1'][0]);
                         setTimeout(function () {
                            message.html('');
                        },2000);
                    }else if (result['message']['pwd2']){
                        message.html(result['message']['pwd2'][0]);
                         setTimeout(function () {
                            message.html('');
                        },2000);

                    }else if(result['message']['__all__']){
                        message.html(result['message']['__all__'][0]);
                         setTimeout(function () {
                            message.html('');
                        },2000);
                    }
                }
            }
        })
    })
};

Auth.prototype.run = function(){
    this.listenSigninEvent();
    this.listenSignupEvent();
};

$(function () {
  var auth = new Auth();
  auth.run();
});
