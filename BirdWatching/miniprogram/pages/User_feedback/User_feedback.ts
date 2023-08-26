// pages/User_feedback/User_feedback.ts
import {create_feedbacks} from '../../components/interface'
const feedapp=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    // 问题反馈
    text:''
  },

    //备注
searchInput:function(e:any){
  this.setData({
    text: e.detail.value,
  })

},

  //提交按钮
  jumpToDetail() {
    var that=this
    wx.showModal({
        title: '提示',
        content: '是否确认提交',
        success: function (res) {
            if (res.confirm) {
                console.log('用户点击确定')
                that.CreatFeedbacks()
                wx.showToast({
                    title: '成功',
                    duration: 1000,
               })
               wx.switchTab({      
                url: '../../pages/mine/mine',
               })      
               that.data.text=''
            }else{
               console.log('用户点击取消')
            }

        }
    })
},

// 用户反馈接口
CreatFeedbacks:function(){
  var date={
    user_id:feedapp.globalData.userid,
    feedback_text:this.data.text,
    openid:feedapp.globalData.openid,
    token:feedapp.globalData.token
  }
  create_feedbacks(date).then(res=>{
    console.log(res);
  })
},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    this.CreatFeedbacks()
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