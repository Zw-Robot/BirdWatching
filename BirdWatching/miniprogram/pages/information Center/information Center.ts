// pages/information Center/information Center.ts
import {get_system_notifications} from '../../components/interface'
const centerapp=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    navList:['系统通知','用户互动'],
    nav_type:0,//默认选中第一个
    isFixed:false,//是否吸顶
    navTop:0,//nav菜单激励顶部距离
    center:[]
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

  // 获取系统通知接口
  getSystem:function(){
    get_system_notifications({}).then(res=>{
      console.log(res);
      this.setData({
        center:res.data
      })
    })
    
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    this.getSystem()
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