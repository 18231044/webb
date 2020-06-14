function register(){

    var username = $.trim($("#usernm").val());
    var password = $.trim($("#pswd").val());
    var repass = $.trim($("#confpswd").val());
    var email = $.trim($("#email").val());
    if(!($("#checkbox").is(":checked"))){
        window.alert("请先阅读《论坛使用手册》");
        return false;
    }
    if(!email.match(/.+@.+\..+/)){
        window.alert("邮箱地址错误。");
        return false;
    }
    if(password.length<6 || password.length>16){
        window.alert("您输入的密码长度不合法，密码长度应为6-16位。");
        return false;
    }
    if(password!=repass){
        window.alert("您两次输入的密码不一致。");
        return false;
    }
    var param = "username=" + username;
    param += "&password=" + password;
    param += "&repassword=" + repass;
    param += "&email=" + email;
    $.post('/register', param, function(data){
        if(data=="ep-err") {
            window.alert("以上填写信息不能为空。");
        }
        else if(data=="username-exist")
            window.alert("该用户名已被注册。");
        else if(data=="email-exist")
            window.alert("该邮箱已被注册。");
        else if(data=="input-error")
            window.alert("您所输入的信息中包含非法字符，请重新输入。");
        else if(data=="reg-success"){
            window.alert("注册成功。")
            //setTimeout('location.reload();',500);
            setTimeout(location.href="/",500);
        }
    })
}
    function doSearch(e){
        if(e != null && e.keyCode != 13)
            return false;
        var keyword = $.trim($("#search").val());
        if( keyword.indexOf('%')>=0 ){
            window.alert('您输入的关键字不合法');
            $("#keyword").focus();
            return false;
        }
        if( keyword.length == 0 ){
            window.alert('关键字不能为空');
            $("#keyword").focus();
            return false;
        }
        if( keyword.length >15 ){
            window.alert('您输入的关键字过长');
            $("#keyword").focus();
            return false;
        }
        location.href = '/search/1-' + keyword ;
        window.event.returnValue=false;
    }

    function login(e) {
        if(e != null && e.keyCode != 13 && e.button != 0){
            return false;
        }
        var username = $.trim($("#username").val());
        var password = $.trim($("#Password").val());
        var param = "username=" + username + "&password=" + password;
        $.post('/login', param, function (data) {
            if(data == "login-fail"){
                window.alert('用户名或密码输入错误。');
                return false;
            }
            else if(data == "login-success"){
                window.alert("登录成功！");
                //setTimeout('location.reload();',500);
                setTimeout(location.href='/',500);
                window.event.returnValue=false;
            }
        });
    }

    function addComment(blogid, ban){
        if(ban == 1){
            window.alert("您已被禁言，无法发布评论。");
            return false;
        }
        var content = $.trim($("#comment").val());
        if(content.length < 5 || content.length >530){
            window.alert("评论内容字数应在5~530字之间。");
            return false;
        }
        var param = 'blogid=' + blogid +'&content=' + content;
        $.post('/comment', param, function(data){
            if(data == 'len-error'){
                 window.alert("评论内容字数应在5~530字之间。");
                return false;
            }
            else if(data=='not-login'){
                window.alert("请先登录");
                location.href='/login';
                window.event.returnValue=false;
                return false;
            }
            else if(data == 'add-success') {
                window.alert("评论成功")
                location.reload();
            }
            else if(data == 'add-fail'){
                 window.alert("评论失败");
                 return false;
            }

        })
    }

    function deletComment(commentid, userid, blogid){
        var param = 'commentid=' + commentid + '&userid=' + userid + '&blogid=' +blogid;
        $.post('/comment/del', param, function(data){
            if(data=='del-success'){
                window.alert("评论删除成功");
                location.reload()
            }
            else if(data=='not-login'){
                window.alert("请先登录");
                location.href='/login';
                window.event.returnValue=false;
                return false;
            }
            else if(data=='del-fail')
                window.alert("评论删除失败");
        })
    }

    function like(commentid) {
        var param = 'commentid=' + commentid;
        $.post('/likes', param, function(data){
            if(data=='have-liked')
                window.alert("您已经点赞过这条评论");
            else if(data=='like-success')
                window.alert("点赞成功");
        })
    }

    function writeblog(){
        var headline = $.trim($("#headline").val());
        var content = $.trim($("#content").val());
        var type = $.trim($("#type").val());
        var level = $.trim($("#level").val());

        if(type=='讨论区')
            type='discuss';
        else if(type=='课程推荐')
            type='commend';
        else if(type=='校园周边')
            type='school';
        else if(type=='刷题区')
            type='do';
        if(level=='无限制')
            level='0';
        else if(type=='1级')
            level='1';
        else if(type=='2级')
            level='2';
        else if(type=='3级')
            level='3';
        else if(type=='4级')
            level='4';
        else if(type=='5级')
            level='5';
        var param = 'headline=' + headline + '&content=' + content + '&type=' +type;
        param += '&level=' + level;
        $.post('/blog/write', param, function(data){
            if(data=='banned'){
                window.alert("您已被禁言,无法发布帖子");
                return false;
            }
            if(data=='content-len-error'){
                window.alert("您输入的帖子内容过多");
                return false;
            }
            else if(data=='headline-len-error'){
                window.alert("您输入的标题过长");
                return false;
            }
            else if(data=='not-login'){
                window.alert("请先登录")
                location.href = '/login';
                window.event.returnValue=false;
                return false;
            }
            else if(data=='level-error'){
                window.alert("帖子阅读等级不能超过自己的等级");
                return false;
            }
            else if(data=='write-success'){
                window.alert("帖子发布成功");
                location.href = '/discuss';
                window.event.returnValue=false;
                return true;
            }
            else if(data=='write-fail'){
                window.alert("帖子发布失败，请稍后再试");
                return false;
            }
        })
    }

    function updateinfo(){
        var nickname = $.trim($("#nickname").val());
        var birthday = $.trim($("#birthday").val());
        var sex = $.trim($("#sex").val());
        if(nickname==''){
            window.alert("昵称不能为空");
            return false;
        }
        var param = 'nickname=' + nickname + '&birthday=' + birthday + '&sex=' + sex;
        $.post('/user/updateinfo', param, function (data) {
            if(data=='nickname-error'){
                window.alert("您输入的昵称过长");
                return false;
            }
            else if(data=='update-success'){
                window.alert("修改成功");
                location.reload();
                return true;
            }
            else if(data=='update-fail'){
                window.alert("修改失败");
                return false;
            }
        })
    }

    function changePassword(userid) {
        var oldpassword = $.trim($("#oldpassword").val());
        var newpassword = $.trim($("#newpassword").val());
        var repassword = $.trim($("#repassword").val());
        if(newpassword.length<6 || newpassword.length>16){
            window.alert("您输入的密码长度不合法，密码长度应为6-16位。");
            return false;
        }
        if(newpassword!=repassword){
            window.alert("您两次输入的密码不一致。");
            return false;
        }
        var param = "oldpassword=" + oldpassword + "&newpassword=" + newpassword + "&repassword=" + newpassword;
        $.post('/chgpw', param, function (data) {
            if(data=='old-new-diff'){
                window.alert("您输入的原密码不正确");
                return false;
            }
            else if(data=='re-diff'){
                window.alert("您两次输入的密码不一致。");
                return false;
            }
            else if(data=='new-len-error'){
                window.alert("您输入的新密码长度不合法，密码长度应为6-16位。");
                return false;
            }
            else if(data=='illegal-error'){
                window.alert("您输入的密码含有非法字符，请重新输入");
                return false;
            }
            else if(data=='change-success'){
                window.alert("修改成功");
                location.href="/home/"+userid;
                return true;
            }
            else if(data=='change-fail'){
                window.alert("修改失败");
                return false;
            }
        })
    }
    function favorite(blogid){
        $.post('/favorite', 'blogid='+blogid, function(data){
            if(data == 'not-login')
                window.alert("请先登录。");
            else if(data == 'favorite-pass'){
                window.alert("收藏成功");
                $('.favorite-btn').text("已收藏");
                $(".favorite-btn").attr('onclick','').unbind('click');
            }
            else{
                window.alert("收藏失败");
            }
        })
    }
    function cancel_f(blogid){
        $.ajax({
            url: '/favorite/' + blogid,
            type: 'delete',
            success: function(data){
                if(data == 'not-login')
                    window.alert("请先登录。");
                else if(data == 'cancel-pass'){
                window.alert("取消收藏成功");
                $('.favorite-btn').text("已取消收藏");
                $(".favorite-btn").attr('onclick','').unbind('click');
                }
                else if(data == 'cancel-fail'){
                    window.alert("取消收藏失败");
                }
            }
        });
    }
    function delete_blog(blogid){
        $.ajax({
            url: '/blog/del/' + blogid,
            type: 'delete',
            success: function(data){
                if(data == 'have-no-right')
                    window.alert("您没有权限进行此操作");
                else if(data == 'del-success'){
                    window.alert("删除成功");
                    location.reload();
                }

            }
        });
    }

    var COMMENTID = 0;

    function toreply(commentid, nickname) {
        $("#replybtn").show();
        $("#commentbtn").hide();
        //$("#comment").val("Reply to "+ nickname + ":   ");
        $("#comment").attr("placeholder","Reply to "+ nickname + ":   ");
        $("#comment").focus();
        COMMENTID = commentid;
    }
    
    function replyComment(blogid) {
        var content = $.trim($("#comment").val());
        if(content.length>530){
            window.alert("您输入的评论过长");
            return false;
        }
        var param = 'blogid=' + blogid + '&content=' +content +'&commentid=' + COMMENTID;
        $.post('/comment/reply', param, function(data){
            if(data=='comment-banned'){
                window.alert('您已被禁言');
                return false;
            }
            else if(data=='len-error'){
                window.alert("您输入的评论过长");
                return false;
            }
            else if(data=='add-success'){
                window.alert("评论成功");
                location.reload();
                return true;
            }
            else if(data=='add-fail'){
                window.alert("评论失败");
                return false;
            }
            else if(data=='not-login'){
                window.alert("请先登录")
                return false;
            }
        })
    }