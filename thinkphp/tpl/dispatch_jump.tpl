{__NOLAYOUT__}<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>跳转提示</title>
    <meta name="viewport" content="initial-scale=1, maximum-scale=1">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <link rel="stylesheet" href="//g.alicdn.com/msui/sm/0.6.2/css/sm.css">
    <link rel="stylesheet" href="//g.alicdn.com/msui/sm/0.6.2/css/sm-extend.css">
  </head>

<body>
<div class="page-group">
        <div class="page page-current">

<header class="bar bar-nav">
    <h1 class="title">币控网提示</h1>
</header>

<div class="content">
<div class="card">
<?php switch($code){ ?>
    <?php case 1:?>
<div class="card-header">操作成功</div>
  <?php break;?>
  <?php case 0:?>
<div class="card-header">操作失败</div>
<?php } ?>
<div class="card-content">
      <div class="card-content-inner" style="font-size:0.8rem;"><?php echo(strip_tags($msg));?></div>
    </div>
<div class="card-footer jump"><small>页面自动 <a id="href" href="<?php echo($url);?>">跳转</a> 等待时间：<b id="wait"><?php echo($wait);?></b></small></div>
  </div>
</div>
    <script type="text/javascript">
        (function(){
            var wait = document.getElementById('wait'),
                href = document.getElementById('href').href;
            var interval = setInterval(function(){
                var time = --wait.innerHTML;
                if(time <= 0) {
                    location.href = href;
                    clearInterval(interval);
                };
            }, 1000);
        })();
    </script>
    </div>
</div>
</body>
</html>
