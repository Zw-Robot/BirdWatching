import { get_show_images ,check_info} from "../../components/interface";
import { request } from "../../components/request";
const homeapp=getApp()

var util = require('../../utils/util.js');
Page({

  /**
   * 页面的初始数据
   */
  data: {
    //存放轮播图数据列表
    swiperList:[],
    fronturl:request.URL+'/inventory/get_file/'
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    //调用轮播图
    this.getSwiperList()
    // 时间
    var time = util.formatTime(new Date());
    this.setData({
      time: time
    });
    homeapp.globalLongin()
  },

  //获取轮播图数据
  getSwiperList(){
    get_show_images().then(res=>{
      this.setData({
        swiperList:res
      })
    })
  },

  //添加记录区域
  gotoAdd(){
    wx.navigateTo({
      url:"/pages/add/add"
    })
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