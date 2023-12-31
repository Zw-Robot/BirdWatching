// pages/storehouse/storehouse.ts

import { get_all_birds, get_all_orders, wx_get_all_birds } from "../../components/interface";
const storeapp=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    //选中
    activeItem:0,
    //搜索
    isSearch:true,
    isClear:false,
    val:'',
    // 鸟列表
    rightMenuList:[],//边侧栏数据
    leftMenuList:[],//鸟库数据
//所有鸟库数据
cates:[],
},

//选中
SyntheSize: function (e:any) {
  let id = e.currentTarget.dataset.item;
  this.setData({
    activeItem: id,
  })
  wx_get_all_birds({order:this.data.rightMenuList[id].name}).then(res=>{
    this.setData({
      leftMenuList:res
    })
  })
},


// 搜索栏区域
getInput:function(e:any){
  this.setData({
    val:e.detail.value
  })
  if(this.data.val.length>0){
    this.setData({
      isSearch:false,
      isClear:true,
    })
  }else{
    this.setData({
      isSearch:true,
      isClear:false,
    })
  }
  wx_get_all_birds({keyword:this.data.val}).then(res=>{
    this.setData({
      leftMenuList:res
    })
  })
},

searchTap:function(){
  wx_get_all_birds({}).then(res=>{
    this.setData({
      leftMenuList:res
    })
  })
},

clearTap:function(){
  this.setData({
    val:'',
    isSearch:true,
    isClear:false,
  })
  wx_get_all_birds({}).then(res=>{
    this.setData({
      leftMenuList:res
    })
  })

},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    this.setData({
      leftMenuList:storeapp.globalData.left
    })
    this.setData({
      rightMenuList:storeapp.globalData.right
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
    this.setData({
      leftMenuList:storeapp.globalData.left
    })
    this.setData({
      rightMenuList:storeapp.globalData.right
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

  },
  })