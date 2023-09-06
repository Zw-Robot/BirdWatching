// pages/account_management/account_management.ts
import { appname, poskey } from "../../components/config";
import { info,wx_get_single_wxusers,delete_info } from "../../components/interface";
const defaultAvatarUrl = 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0'
const accountapp=getApp()
const chooseLocation = requirePlugin('chooseLocation');

Page({

  /**
   * 页面的初始数据
   */
  data: {
    // 性别
    sex: [{
      id: 1,
      value: '男',
      checked:false
    }, {
      id: 2,
      value: '女',
      checked:false
    }],

    geneder:'',
    i:0,
    name:'', //姓名
    address:accountapp.globalData.address, //地点
    longitude:accountapp.globalData.longitude,
    latitude:accountapp.globalData.latitude,
    region:'',
    phone:'', // 联系电话
    email:'', //邮箱

    // 用户信息
    usermessage:[],
    nickname:'',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    canIUseGetUserProfile: false,
    canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl') && wx.canIUse('open-data.type.userNickName'), // 如需尝试获取用户信息可改为false
    avatarUrl: defaultAvatarUrl,
    loc:{},
  },

  // 获取用户信息接口
  getSingleUsers:function(){
    var date={
      user_id:accountapp.globalData.userid,
      openid:accountapp.globalData.openid,
      token:accountapp.globalData.token
    }
    wx_get_single_wxusers(date).then(res=>{
      console.log(res);
      this.setData({
        usermessage:res.data,
        nickname:res.data.avatar,
        name:res.data.name,
        phone:res.data.phone,
        email:res.data.email,
        geneder:res.geneder,
        i:res.i,
      })
      for (let index = 0; index < this.data.sex.length; index++) {
        this.data.sex[this.data.i].checked=true
      }
    })
    
  },

  // 头像
  onChooseAvatar(e:any) {
    const { avatarUrl } = e.detail 
    this.setData({
      avatarUrl,
    })
  },
  getUserProfile() {
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认，开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '展示用户信息', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        console.log(res)
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    })
  },
  getUserInfo(e: any) {
    // 不推荐使用getUserInfo获取用户信息，预计自2021年4月13日起，getUserInfo将不再弹出弹窗，并直接返回匿名的用户个人信息
    console.log(e)
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },

  // 昵称
  getUserName(e:any) {
    console.log(e.detail.value);  //用户输入或者选择的昵称
    this.setData({
      nickname:e.detail.value
    })
  },

  // 姓名
  getname:function(e:any){
    this.setData({
      name:e.detail.value
    })
  },

  // 性别
  radioChange: function (e:any) {
    const sex = this.data.sex
    for (let i = 0, len = sex.length; i < len; ++i) {
      sex[i].checked = sex[i].id == e.detail.value
      if (sex[i].checked==true) {
        console.log(sex[i].value);
        this.setData({
          geneder:sex[i].value
        })
      }
    }
  },

  // 地点
  getAddress:function(){
    this.setData({
      address:accountapp.address,
      longitude:accountapp.longitude,
      latitude:accountapp.latitude,
    })
  },
  ChoosePoint:function()
  { 
    const key = poskey
    const referer = appname
    const category = '';
    const location = JSON.stringify({
      latitude: accountapp.globalData.latitude,
      longitude:accountapp.globalData.longitude
    });
    wx.navigateTo({
      url: 'plugin://chooseLocation/index?key=' + key + '&referer=' + referer + '&location=' + location + '&category=' + category
    });
  },
  getUserProvince:function(e:any)
  {
    this.setData({
      region:e.detail.value
    })
    console.log(this.data.region);
    
  },

  // 联系电话
  getphone:function(e:any){
    this.setData({
      phone:e.detail.value
    })
  },

  // 邮箱
  getemail:function(e:any){
    this.setData({
      email:e.detail.value
    })
  },

  // 提交
  onloud:function(){
    if(!this.data.nickname || !this.data.name || !this.data.geneder || !this.data.phone || !this.data.email){
      wx.showModal({
        title:'提示',
        content:'信息尚未填写！'
      })
      return
    }
    let loc = chooseLocation.getLocation();
    console.log(loc);
    if (!loc){
      loc=accountapp.globalData.address_component
    }
    var data={
      userInfo:{
        username:this.data.nickname,
        city:loc.city,
        country:loc.district,
        province:loc.province,
        gender:this.data.geneder
      },
      name:this.data.name,
      phone:this.data.phone,
      email:this.data.email,
      openid:accountapp.globalData.openid,
      token:accountapp.globalData.token
    }
    console.log(data);
    info(data).then(res=>{
      console.log(res);
    })
    if(this.data.phone.length!=11){
      wx.showModal({
        title: '提示',
        content: '电话填写错误！',
      })
    }else if (this.data.avatarUrl='') {
      wx.showModal({
        title: '提示',
        content: '请获取头像！',
      })
    }else{
      wx.showModal({
        title: '提示',
        content: '注册成功!',
      })
      wx.switchTab({      
        url: '../../pages/home/home',
      }) 
    }
  },

  // 退出登录按钮
  goout:function(){
    var date={
      openid:accountapp.globalData.openid,
      token:accountapp.globalData.token,
    }
    delete_info(date).then(res=>{
      console.log(res);
    })
    wx.showModal({
      title: '提示',
      content: '退出成功!',
    })
    wx.switchTab({      
      url: '../../pages/home/home',
    }) 
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    this.getSingleUsers()
    this.setData({
      address:accountapp.address,
      longitude:accountapp.longitude,
      latitude:accountapp.latitude,
    })
    // 头像
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
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
    const loc = chooseLocation.getLocation();
    console.log(loc);
    this.setData({
      loc:loc,
    })
    if(loc){
      var add = loc.address + loc.name
      var log = loc.longitude
      var lat = loc.latitude
    }else{
      var add = accountapp.globalData.address
      var log = accountapp.globalData.longitude
      var lat = accountapp.globalData.latitude
    }
    try{
      this.setData({
        address:add,
        longitude:log,
        latitude:lat,
      });
    }
    catch{
      this.setData({
        address: "",
        latitude: 0.0,
        longitude: 0.0,
        weather:'',
        temperature:0
      });
    }
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