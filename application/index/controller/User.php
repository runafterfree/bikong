<?php
namespace app\index\controller;
use app\index\controller\Base;
use \think\Validate;
use \think\Session;
use \think\Db;

class User extends Base
{
    public function  _initialize()
    {
        parent::_initialize();
        $login_actions = ['center','savePriceNotify','delpid'];

        if(empty($this->user) && in_array($this->action, $login_actions))
        {
            if($this->isAjax)die('没有登录');
            $this->error('请先登陆','/user/login/');
        }
    }
    //用户注册
    public function reg()
    {
        if($this->isPost)
        {
            $re = $this->checkValid('add');
            if($re!='success')
                $this->error($re, '/user/reg/');

            $sql = "INSERT INTO b_user(name,pwd,tel,reg_time) VALUES(:name,:pwd,:tel,:reg_time)";
            $tel = Session::get('reg_tel');
            Db::execute($sql,['name'=>$this->param['name'],'pwd'=>md5($this->param['pwd']),
                'tel'=>$tel, 'reg_time'=>time()]);

            $this->success('注册成功','/user/login/');
        }
        return $this->fetch('user/reg');
    }

    //用户登陆
    public function login()
    {
        if($this->isPost)
        {
            $user = Db::table('b_user')->field('uid,name,tel,pwd')->where(['name'=>$this->param['name']])->find();
            if(empty($user) || $user['pwd']!=md5($this->param['pwd']))
                $this->error('用户名或密码不正确', '/user/login');
            Db::execute("UPDATE b_user set last_login=UNIX_TIMESTAMP() WHERE uid=".$user['uid']);
            unset($user['pwd']);
            Session::set('user', $user);
            $this->success('登陆成功','/user/center/');
        }

        return $this->fetch('user/login');
    }

    //用户中心
    public function center()
    {
        //获得价格通知
        //$data = Db::table('b_price_notify')->where(['uid'=>$this->user['uid']])->field('pid,uid,note,tel,add_time')->order('step asc')->select();
        $data = Db::table('b_price_notify')->field('pid,uid,note,tel,add_time,op,price')->order('add_time desc')->select();
        $list = [];
        foreach($data as $val)
        {
            //$val['note'] = str_replace(array('当前','，请尽快处理'),'',$val['note']);
            $list[] = $val;
        }
        $this->assign('list', $list);

        //获得站点

        //获得上线通知

        return $this->fetch('user/center');
    }

    public function getSpec($site_id)
    {
        $data = Db::table('b_spec')->where(['site_id'=>$site_id,'active'=>1])->field('spec_id, spec_name,spec_long,price')->select();
        if(!$data)
        {
            if($this->isAjax) die(array('status'=>'failed'));
            return false;
        }
        $arr = array();
        foreach($data as $val)
        {
            $arr[$val['spec_id']] = $val['spec_long'].'('.$val['spec_name'].'当前价格：'.floatval($val['price']).'元)';
        }
        if($this->isAjax) die(json_encode(array('status'=>'success','data'=>$arr)));
        return $arr;
    }

    public function logout()
    {
        Session::set('user',null);
        $this->redirect('/user/login/');
    }

    public function savePriceNotify()
    {
        $site = \think\Config::get('site');
        $site_id = $this->param['site_id'];
        if(empty($site_id) || !isset($site[$site_id]))
            die(json_encode(array('status'=>'站点不存在')));
        $spec_id = $this->param['spec_id'];
        if(empty($spec_id))
            die(json_encode(array('status'=>'币种不存在')));
        $spec = Db::table('b_spec')->find($spec_id);
        if(!$spec)
            die(json_encode(array('status'=>'币种不存在')));
        $price = $this->param['price'];
        if(empty($price))
            die(json_encode(array('status'=>'错误的价格')));
        $price = floatval($price);
        $op = $this->param['op'];

        $note = $site[$site_id];
        $note .= $spec['spec_long'].'('.$spec['spec_name'].')当前价格';
        $note .= $op ? '小于' : '大于';
        $note .= $price.'元，请尽快处理！';
        $add_time = time();
        
        Db::execute("INSERT INTO b_price_notify(uid,spec_id,op,note,tel,add_time,price) VALUES(:uid,:spec_id,:op,:note,:tel,:add_time,:price)",['uid'=>$this->user['uid'],'spec_id'=>$spec_id,'op'=>$op,'note'=>$note,'tel'=>$this->user['tel'],'add_time'=>$add_time,'price'=>$price]);
        $pid = Db::table('b_price_notify')->getLastInsID();
        $add_time = date('Y-m-d H:i',$add_time);
        $note .= '&nbsp;&nbsp;(<small>触发条件：价格'.($op ? '小于':'大于').$price.'元）</small>';
        $content = <<<EOT
<div class="card item{$pid}">
            <div class="card-content">
              <div class="card-content-inner">短信内容：{$note}<br />
              <small>手机号：{$this->user['tel']}&nbsp;&nbsp;添加时间：{$add_time}</small>
              </div>
            </div>
            <div class="card-footer"><a class="link" href="javascript:del({$pid})">删除</a></div>
</div>
EOT;
        die(json_encode(array('status'=>'success','content'=>$content)));
    }

    public function delpid()
    {
        $pid = intval($this->param['pid']);
        if(!$pid)
            die('数据错误');
        $notify = Db::table('b_price_notify')->find($pid);
        if(!$notify || $notify['uid']!=$this->user['uid'])
            die('数据错误或无权限');
        Db::table('b_price_notify')->delete($pid);
        die('success');
    }

    public function checkValid($scene='add')
    {
        $validation = new Validate([
            'name'=>'require|min:6|max:30|db_unique',
            'pwd'=>'require|min:8|max:30|confirm:pwd_confirm',
            'tel'=>'require|tel_unique',
            'valicode'=>'require|same',
        ],[
            'name.require'=>'用户名不能为空',
            'name.min'=>'用户名在6-20个字符',
            'name.max'=>'用户名在6-20个字符',
            'pwd.min'=>'密码在8到30字符',
            'pwd.max'=>'密码在8到30字符',
            'pwd.confirm'=>'两次输入的密码不一致',
            'tel.require'=>'手机号不能为空',
            'valicode.require'=>'验证码不能为空',
        ]);
        $validation->extend('same',function($value){
            $limit = Session::get('limit');
            if(!isset($limit['valicode']) || $value!=$limit['valicode'])
                return '验证码不正确';
            return true;
        });
        $validation->extend('db_unique',function($value){
            $data = Db::table('b_user')->field('uid')->where(['name'=>$value])->find();
            return !$data ? true : '用户名已存在';
        });
        $validation->extend('tel_unique',function($value){
            if(!preg_match('/^1\d{10}$/', $value))
                return '手机格式不正确';
            $data = Db::table('b_user')->field('uid')->where(['tel'=>$value])->find();
            return !$data ? true : '手机号已注册';
        });
        $validation->scene('add',['name','pwd','tel','valicode']);
        //$validation->scene('reg', ['name','pwd', 'tel','valicode']);
        $result = $validation->batch()->check($this->param);
        if(!$result){
            if($this->isAjax)
            {
                echo implode('<Br />',$validation->getError());
            }
            else
            {
                return implode('<Br />',$validation->getError());
            }
        }
        else
        {
            if($this->isAjax)
            {
                echo 'success';
            }
            else
            {
                return true;
            }
        }
    }


}
