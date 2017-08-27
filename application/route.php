<?php
// +----------------------------------------------------------------------
// | ThinkPHP [ WE CAN DO IT JUST THINK ]
// +----------------------------------------------------------------------
// | Copyright (c) 2006~2016 http://thinkphp.cn All rights reserved.
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: liu21st <liu21st@gmail.com>
// +----------------------------------------------------------------------

return [
    '[user]'=> [
        '/savePriceNotify/'=>['index/user/savePriceNotify'],
        '/getSpec/' =>['index/user/getSpec'],
        '/reg/' => ['index/user/reg'],
        '/login/' => ['index/user/login'],
        '/findpwd/'=>['index/user/findpwd'],
        '/checkValid/'=>['index/user/checkValid'],
        '/center/'=>['index/user/center'],
        '/delpid/'=>['index/user/delpid'],
        '/logout/'=>['index/user/logout'],
    ],
    '[base]'=>[
        '/valicode/'=>['index/base/valicode'],
    ],
];
