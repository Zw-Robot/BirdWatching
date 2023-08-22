// pages/attendRace/attendRace.ts
import {create_group,add_group,get_all_matches, wx_user_group, exit_group} from '../../components/interface'
const attendapp=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    eye:false,
    //比赛信息
    match_id:'',
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
    add_group_name:'',
    add_password:'',
    result:'',
    creat_result:'',
    creat_hidde:true
  },

  switch() {
    this.setData({
      eye:!this.data.eye
    })
  },

  //创建小组
  modalinput: function () {
    this.setData({
      hiddenmodalput: !this.data.hiddenmodalput,
      group_name:'',
      add_password:'',
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
      add_password:e.detail.value
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
    console.log(e.detail.value);
    
  },

  //创建小组接口
  creatGroup:function(){
    var date={
      match_id:this.data.match_id,
      group_name:this.data.group_name,
      group_desc:'111',
      group_user:'222',
      password:this.data.add_password,
      user_id:attendapp.globalData.userid,
      openid:attendapp.globalData.openid,
      token:attendapp.globalData.token
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
    console.log(attendapp.globalData);
    
    var date={
      user_id:attendapp.globalData.userid,
      openid:attendapp.globalData.openid,
      token:attendapp.globalData.token,
      group_name:this.data.add_group_name,
      password:this.data.add_password,
    }
    console.log(date);
    
    add_group(date).then(res=>{
      console.log(res);
      wx.showModal({
        title:res.msg
      })
    })


  },

  getAllGroup:function(){
    var date={
      user_id:attendapp.globalData.userid
    }
    wx_user_group(date).then((res: any)=>{
      if(res.data.length > 0){
        this.setData({creat_hidde:false})
      }
    })
  },

  exitGroup:function(){
    var date={
      user_id:attendapp.globalData.userid,
      openid:attendapp.globalData.openid,
      token:attendapp.globalData.token,
    }
    exit_group(date).then(res=>{
      console.log(res);
      wx.showModal({
        title:res.msg
      })
      this.setData({
        creat_hidde:true
      })
    })
  },
  getAllMatch:function(){
    var date={
      match_id :2,
    }
    get_all_matches(date).then(res=>{
      console.log(res);
      this.setData({
        match_id:res[0].match_id,
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
    this.getAllGroup()
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