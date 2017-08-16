<?php
namespace app\index\controller;
use app\index\controller\Base;

class User extends Base
{
    public function reg()
    {
        return $this->fetch('user/reg');
    }
}
