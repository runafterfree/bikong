<?php
namespace app\index\controller;
use app\index\controller\Base;
use \think\Db;

class Index extends Base
{
    public function index()
    {
        //获得站点公告
        $notice = Db::table('b_notice')->field('title,site_id,link,is_online,update_time')->order('update_time DESC')->limit(10)->select();
        $this->assign('notice', $notice);
        
        return $this->fetch();
    }
}
