<?php
namespace app\index\controller;
use \think\Controller;
use \think\Session;
use \think\Request;
class Base extends Controller
{
    public function _initialize()
    {
        $request = Request::instance();
        $this->isPost = $request->method()=='POST' ? 1 : 0;
        $this->isAjax = $request->isAjax();
        $this->param = $request->param();
    }
    //生成手机验证码
    public function valicode()
    {
        $valicode = mt_rand(100000,999999);
        Session::set('valicode', $valicode);
        Session::set('reg_tel', $this->param['tel']);
        $send_time = Session::get('send_time', 0);
        if($send_time)
            Session::set('send_time', $send_time+1);

        //Session::set('valicode', '111111');
        //Session::set('reg_tel', '13798251605');
        echo 1;
        exit;
    }
}
