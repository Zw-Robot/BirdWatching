// pages/add/add.ts
const checkappright=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data:{
    checkedList:['1',checkappright.globalData.checkedList],
    //灰色顶部
    navList:['待添加鸟类',checkappright.globalData.checkedList],
    nav_type:0,//默认选中第一个
    isFixed:false,//是否吸顶
    navTop:0,//nav菜单激励顶部距离
    
    region:[],//存放地点
    Number:0,//数量
    number:0//人数
  },
  //灰色顶部
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

  //提交按钮
  jumpToDetail() {
    wx.showModal({
        title: '提示',
        content: '是否确认提交',
        success: function (res) {
            if (res.confirm) {
                console.log('用户点击确定')
                wx.showToast({
                    title: '成功',
                    duration: 1000,
                    success: function () {
                    setTimeout(function () {
                    wx.reLaunch({
                    url: '../index/index',
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

  // 添加时间
  bindDateChange: function(e:any) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      date: e.detail.value
    })
  },

  // 添加地点
  getUserProvince:function(e:any)
  {
     this.setData({
         region:e.detail.value
     })
  },

  //添加数量
  addNumber:function(){
    this.setData({
      Number:this.data.Number+1
    })
  },
  //减少数量
  subtract:function(){
    this.setData({
      Number:this.data.Number<=0? 0:this.data.Number-1
    })
  },
  //添加人数
  add:function(){
    this.setData({
      number:this.data.number+1
    })
  },
  //减少人数
  subtractnumber:function(){
    this.setData({
      number:this.data.number<=0? 0:this.data.number-1
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad:function() {
    this.setData({
      checkedList:checkappright.globalData.checkedList
    })
    this.setData({
      navList:checkappright.globalData.checkedList
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady:function() {
    wx.setNavigationBarTitle({
      title:'新增记录'
    })
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow:function() {
    this.setData({
      checkedList:checkappright.globalData.checkedList
    })
    this.setData({
      navList:checkappright.globalData.checkedList
    })
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