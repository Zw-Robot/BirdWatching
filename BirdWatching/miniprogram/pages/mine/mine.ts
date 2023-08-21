// pages/mine/mine.ts
import {get_all_bird_records, info,wx_get_record,get_score} from '../../components/interface'
const mineapp = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    userid:mineapp.globalData.openid,
    record:[],
    navList:['观鸟记录','我的活动'],
    nav_type:0,//默认选中第一个
    isFixed:false,//是否吸顶
    navTop:0,//nav菜单激励顶部距离

    //用户信息
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    canIUseGetUserProfile: false,
    canIUseOpenData: true,
    recordMessage:[],
    level:0,
  },

  changeType(e:any){
    let{index}=e.currentTarget.dataset;
    if(this.data.nav_type==index||index==undefined) return;
    this.setData({
      nav_type:index,
    })
    if(this.data.isFixed){
      wx.pageScrollTo({
        selector:'#content',
        duration:0.5
      })
    }
  },

  getAllBirdRecords:function(){
    console.log(mineapp.globalData.userid);
    var date={
      user_id:mineapp.globalData.userid,
    }
    wx_get_record(date).then(res=>{
      console.log(res);
      this.setData({
        recordMessage:res,
        record:res.data
      })
    })
    
  },

  // 事件处理函数
  bindViewTap() {
    wx.navigateTo({
      url: '../logs/logs',
    })
  },

  // 用户等级
  getScore:function(){
    var date={
      userid:mineapp.globalData.userid,
      openid:mineapp.globalData.openid,
      token:mineapp.globalData.token
    }
    get_score(date).then(res=>{
      this.setData({
        level:res.level
      })
    })
  },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    this.getUserProfile()
    this.getScore()
    this.getAllBirdRecords()
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
  },

  getUserProfile() {
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认，开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '展示用户信息', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        console.log(res)
        this.setData({
          rawData:res.rawData,
          signature:res.signature,
          iv:res.iv,
          encryptedData:res.encryptedData,
          userInfo: res.userInfo,
          hasUserInfo: true,
        })
        res['openid'] = mineapp.globalData.openid
        res["token"]  = mineapp.globalData.token
        console.log(res);
        
        info(res).then(res=>{
          console.log(res);
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

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {
    wx.createSelectorQuery().select("#nav").boundingClientRect((rect)=>{
      if(rect && rect.top){
        this.setData({
          navTop:parseInt(rect.top)
        })
      }
    }).exec()
  },

  onPageScroll(e:any){
    let scrollTop=parseInt(e.scrollTop),
    isFixed=scrollTop>=this.data.navTop;
    if(this.data.isFixed !== isFixed){
      this.setData({
        isFixed
      })
    }
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