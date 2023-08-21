// pages/attendRace/attendRace.ts
import {create_group,add_group,get_all_groups,get_all_matches} from '../../components/interface'
const attendapp=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    //比赛信息
    match_name:'',
    match_desc:'',
    start_time:'',
    end_time:'',
    creat_at:'',
    match_create:'',
    match_location:'',
    referee:'',
    //初始化隐藏模态输入框
    hiddenmodalput: true,
    hiddenmodalputright: true,
    group_name:'',
    password:'',
    add_group_name:'',
    add_password:'',
    result:'',
    creat_result:'',
    creat_hidde:true
  },

  //创建小组
  modalinput: function () {
    this.setData({
      hiddenmodalput: !this.data.hiddenmodalput,
      group_name:'',
      password:'',
    })
  },
  //提交
  confirm: function () {
    this.creatGroup()
    this.setData({
      hiddenmodalput: !this.data.hiddenmodalput
    })
  },
  //加入小组
  modalinputright: function () {
    this.setData({
      hiddenmodalputright: !this.data.hiddenmodalputright,
      add_group_name:'',
      add_password:'',
    })
  },
  //提交
  confirmright: function () {
    this.setData({
      hiddenmodalputright: !this.data.hiddenmodalputright
    })
    this.addGroup()
  },

  get_group_name:function(e:any){
    this.setData({
      group_name:e.detail.value
    })
  },

  get_group_password:function(e:any){
    this.setData({
      password:e.detail.value
    })
  },

  add_group_name:function(e:any){
    this.setData({
      add_group_name:e.detail.value
    })
  },

  add_group_password:function(e:any){
    this.setData({
      add_password:e.detail.value
    })
  },

  leave_group:function(){
    this.setData({
      creat_hidde:true
    })
    wx.showModal({
      title:'退出成功'
    })
  },

  //创建小组接口
  creatGroup:function(){
    var date={
      match_id:1,
      group_name:this.data.group_name,
      group_desc:'111',
      group_user:'222',
      password:this.data.password,
      userid:attendapp.globalData.userid
    }
    create_group(date).then(res=>{
      console.log(res);
      this.setData({
        creat_result:res.code
      })
      if (this.data.creat_result=='0'){
        wx.showModal({
          title:'创建成功'
        })
        this.setData({
          creat_hidde:false
        })
      }else{
        wx.showModal({
          title:'已存在此小组'
        })
      }
    })
  },

  addGroup:function(){
    var date={
      group_name:this.data.add_group_name,
      user_id:attendapp.globalData.userid,
      openid:attendapp.globalData.openid,
      token:attendapp.globalData.token,
      password:this.data.add_password,
    }
    add_group({date}).then(res=>{
      console.log(res);
      this.setData({
        result:res.code
      })
    })
    if (this.data.result='0') {
      wx.showModal({
        title:'加入成功'
      })
      this.setData({
        creat_hidde:false
      })
    }else{
      wx.showModal({
        title:'没有此小组'
      })
    }
  },

  getAllGroup:function(){
    var date={
      page: 1,
      per_page: 20
    }
    get_all_groups(date).then(res=>{
      console.log(res);
    })
  },

  getAllMatch:function(){
    var date={
      match_id :2,
    }
    get_all_matches(date).then(res=>{
      console.log(res);
      this.setData({
        match_name:res[0].match_name,
        match_desc:res[0].match_desc,
        start_time:res[0].start_time,
        end_time:res[0].end_time,
        creat_at:res[0].creat_at,
        match_create:res[0].match_create,
        match_location:res[0].match_location,
        referee:res[0].referee,
      })
      console.log(res[0].match_desc);
      
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    this.getAllGroup()
    this.getAllMatch()
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})