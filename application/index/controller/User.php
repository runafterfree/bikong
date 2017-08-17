<?php
namespace app\index\controller;
use app\index\controller\Base;
use \think\Validate;
use \think\Session;

class User extends Base
{
    public function reg()
    {
        return $this->fetch('user/reg');
    }


    public function checkValid($scene='add')
    {
        if($scene=='add')
        {
            $validation = new Validate([
                'name'=>'require|min:6|max:30',
                'pwd'=>'require|min:8|max:30|confirm:pwd_confirm',
                'tel'=>'regex:1\d{10}',
                'valicode'=>'same',
            ],[
                'name.require'=>'用户名不能为空',
                'name.min'=>'用户名在6-30个字符长度之间',
                'name.max'=>'用户名在6-30个字符长度之间',
                'pwd.min'=>'密码长度在8到30字符之间',
                'pwd.max'=>'密码长度在8到30字符之间',
                'pwd.confirm'=>'两次输入的密码不一致',
                'tel.regex'=>'请填入有效的手机号',
            ]);
            $validation->extend('same',function($value){
                return $value==Session::get('valicode') ? true : '验证码不正确';
            });
            $result = $validation->batch()->check($this->param);
            if(!$result){
                var_dump($validation->getError());
            }
        }
    }


}
