<?php
namespace app\index\controller;
use app\index\controller\Base;
use \think\Validate;

class User extends Base
{
    public function reg()
    {
        return $this->fetch('user/reg');
    }


    public function checkValid($scene='add')
    {
    }
}
