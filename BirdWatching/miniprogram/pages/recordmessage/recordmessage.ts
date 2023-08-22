// pages/recordmessage/recordmessage.ts
import {wx_get_record,delete_bird_record} from '../../components/interface'
import { request } from '../../components/request'
const recordapp = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    query:'',
    record:{},
    fronturl:request.URL+'/inventory/get_file/'
  },

  getAllBirdRecords:function(){
    var date={
      user_id:recordapp.globalData.userid,
      recordid:this.data.query
    }
    wx_get_record(date).then(res=>{
      console.log(res.data);
      this.setData({
        record:res.data[0]
      })
      
    })
  },

  // 删除鸟类记录接口
  deleteBirdRecord:function(){
    
    var date={
      record_id:this.data.query
    }
    delete_bird_record(date).then(res=>{
      console.log(res);
    })
      
  },

  //删除按钮
  deleteButton:function(){
    const that=this
    wx.showModal({
      title: '提示',
      content: '是否确认删除',
      success: function (res) {
          if (res.confirm) {
              console.log('用户点击确定')
              that.deleteBirdRecord()
              wx.showToast({
                  title: '成功',
                  duration: 1000,
                  success: function () {
                  setTimeout(function () {
                  wx.reLaunch({
                  url: '../../pages/mine/mine',
                    })
                  }, 1000);
               }
             })
                                                      
          }else{
             console.log('用户点击取消')
          }

      }
  })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad:function(options) {
    this.setData({
      query:options.id
    })
    console.log(this.data.query);
    this.getAllBirdRecords()
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