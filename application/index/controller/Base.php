<?php
namespace app\index\controller;
use think\Controller;
use think\Session;
class Base extends Controller
{
    //�����ֻ���֤��
    function valicode()
    {
        $valicode = mt_rand(100000,999999);
        Session::set('valicode', $valicode);
        echo 1;
        exit;
    }
}
