function Message() {

}



Message.prototype.listenMessageEvent = function(){
   var messageBtn = $('.messaage-sunmit');
   messageBtn.click(function () {
        var content = $('.message-content').val();
        $.ajax({
            url: '/message/',
            type: 'POST',
            data: {
                'content': content,
            },
            success: function (data) {
                window.location.reload();
            }
        })
    });
};

Message.prototype.run = function(){
    this.listenMessageEvent();
};

$(function () {
  var message = new Message();
  message.run();
});
