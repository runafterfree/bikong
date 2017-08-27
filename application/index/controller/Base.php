<?php
namespace app\index\controller;
use \think\Controller;
use \think\Session;
use \think\Request;
use \think\Db;
use \Yunpian\Sdk\YunpianClient;
class Base extends Controller
{
    public function _initialize()
    {
        $request = Request::instance();
        $this->isPost = $request->method()=='POST' ? 1 : 0;
        $this->isAjax = $request->isAjax();
        $this->param = $request->param();
        $this->user = Session::get('user');
        $this->action = $request->action();
    }
    //生成手机验证码
    public function valicode()
    {
        if(!$this->isAjax)
            die('非法请求');
        if(!preg_match('/^1\d{10}$/', $this->param['tel']))
            die('手机号码格式不正确');
        $has_tel = Db::table('b_user')->field('uid')->where(['tel'=>$this->param['tel']])->find();
        if($has_tel)
            die('手机号已注册');

        $limit = Session::get('limit');
        if($limit && $limit['send_times']>2 && $limit['expire']<time())
            die('已申请多次验证码，请稍后再试');

        $valicode = mt_rand(100000,999999);

        if(!$this->sendtel($this->param['tel'], '您的验证码是'.$valicode.'。如非本人操作，请忽略本短信。'))
            die('发生未知错误');
        

        if($limit && $limit['expire']<time()+7200)
        {
            $limit['send_times'] += 1;
        }
        else
        {
            $limit = ['send_times'=>1, 'expire'=>(time()+7200)];
        }
        Session::set('limit', $limit);

        echo 'success';
        exit;
    }

    public function sendtel($tel,$msg)
    {
        $clnt = YunpianClient::create('304ab9c0aa24a69869052441f9afbe08');
        $param = [YunpianClient::MOBILE => $tel,YunpianClient::TEXT => '【币控网】'.$msg];
        $r = $clnt->sms()->single_send($param);
        if(r.code())
        {
            return false;
        }
        return true;
    }
}
