function Detail() {
    this.pid = '';
}


//监听点赞事件
Detail.prototype.ListenLikeEvent = function () {
    var likeBtn = $('#like-btn');
    var article_id = likeBtn.attr('data-article-id');
    var like = $('#diggnum');
    likeBtn.click(function () {
        var like_num = like.html();
        if (likeBtn.attr("data-username")) {
            $.ajax({
                url: '/like/',
                type: 'POST',
                data: {
                    'article_id': article_id
                },
                success: function (data) {
                    if (data['state'] === true) {
                        like_num = parseInt(like_num)+1;
                        like.html(like_num);
                        $('.like-text').html('点赞成功！');

                        setTimeout(function () {
                            $('.like-text').html('');
                        }, 2000)
                    } else {
                        $('.like-text').html('你已经点赞过了！');

                        setTimeout(function () {
                            $('.like-text').html('');
                        }, 2000)
                    }
                }
            })
        } else {
            location.href = '/log_page/'
        }
    })
};


//监听评论提交事件
Detail.prototype.ListenCommentBtnEvent = function () {
    commentBtn = $('.comment-btn');
    var self = this;
    commentBtn.click(function () {
        var article_id = $('#like-btn').attr('data-article-id');
        var content = $('#comment_content').val();
        if (self.pid) {
            var index = content.indexOf('\n');
            content = content.slice(index + 1)//发送内容去掉@用户名
        }
        $.ajax({
            url: '/comment/',
            type: 'POST',
            data: {
                'article_id': article_id,
                'content': content,
                'pid': self.pid
            },
            success: function (data) {
                var pub_time = data.pub_time;
                var content = data.content;
                var username = data.username;
                var avatar = data.avatar;
                //动态暂时显示刚发评论
                comment = '<li class="fb" ><ul><p class="fbtime"><img src="' + '/media/avatar/' + avatar + '" style="width: 50px;height: 50px;border-radius: 50%;float: left;margin-left: -60px;margin-top: 10px;"><span style="margin-right: 10px">' + pub_time + '</span>' + username + '</p><p class="fbinfo">' + content + '</p></ul></li>';
                $('#comments').append(comment);

                self.pid = '';
            }
        })
    });
};


//监听回复事件
Detail.prototype.ListenReplyEvent = function () {
    replyBtn = $('.reply-btn');
    var self = this;
    replyBtn.click(function () {

        $('#comment_content').focus();
        var v = '@' + $(this).attr('username') + '\n';
        $('#comment_content').val(v);

        self.pid = $(this).attr('comment_id');
    })
};


//处理富文本内容
Detail.prototype.ListenEditor = function () {
    var article_id = $(".article-content").attr("article_id");
    var article = $(".article-content").attr("content");
    $(".article-content").html(article);
};


Detail.prototype.run = function () {
    this.ListenLikeEvent();
    this.ListenCommentBtnEvent();
    this.ListenReplyEvent();
    this.ListenEditor();
};


$(function () {

    var detail = new Detail();
    detail.run();
});
