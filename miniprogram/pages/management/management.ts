// pages/management/management.ts
const managementapp=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  //提交按钮
  jumpToDetail() {
    wx.showModal({
        title: '提示',
        content: '是否确认退出',
        success: function (res) {
            if (res.confirm) {
                console.log('用户点击确定')
                wx.showToast({
                    title: '成功',
                    duration: 1000,
               })
               wx.switchTab({      
                url: '../../pages/mine/mine',
              })  
              managementapp.globalData.userInfo={}
              console.log(managementapp.globalData.userInfo);
              
            }else{
               console.log('用户点击取消')
            }

        }
    })
},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {

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