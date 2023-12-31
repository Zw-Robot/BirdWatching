import { BirdRecord } from "../../models/birdrecord";
const app=getApp()


let currentDate = new Date();

let hours = currentDate.getHours().toString().padStart(2, '0');
let minutes = currentDate.getMinutes().toString().padStart(2, '0');

let currentTime = hours + ':' + minutes;

let year = currentDate.getFullYear().toString();
let month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
let day = currentDate.getDate().toString().padStart(2, '0');

let currentDateString = year + '-' + month + '-' + day;

import { get_all_orders, wx_get_all_birds } from "../../components/interface";

Page({

  /**
   * 页面的初始数据
   */
  data: {
    //搜索
    isSearch:true,
    isClear:false,
    val:'',
    // 鸟列表
    rightMenuList:[],//边侧栏数据
    leftMenuList:[],//鸟库数据
    latitude:app.globalData.latitude,
    longitude:app.globalData.longitude,
    address:app.globalData.address,
},

//所有鸟库数据
cates:[],

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
  wx_get_all_birds().then(res=>{
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

// 复选框的选中事件
HandelItemChange(e:any){
  const checkedList = e.detail.value.map((value: string) => {
    const [species, id] = value.split('_');
    return {
      species: species,
      id: id
    };
  });
  //获取被选中的复选框的值
  const user_id = app.globalData.userid
  const longitude = app.globalData.longitude
  const latitude = app.globalData.latitude
  const address = app.globalData.address
  const temperature = Number(app.globalData.temperature)
  const weather = app.globalData.weather
  app.globalData.messageList = []
  app.globalData.checkedList = []
  for(const val of checkedList){
    const id = val.id 
    const br:BirdRecord = new BirdRecord(user_id,id,val.species,currentDateString,currentTime,longitude,latitude,address,temperature,weather)
    
    app.globalData.messageList.push(br)
    app.globalData.checkedList.push(val.species)
  }
},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    this.setData({
      leftMenuList:app.globalData.left
    })
    this.setData({
      rightMenuList:app.globalData.right
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {
    this.setData({
      leftMenuList:app.globalData.left
    })
    this.setData({
      rightMenuList:app.globalData.right
    })
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    this.setData({
      leftMenuList:app.globalData.left
    })
    this.setData({
      rightMenuList:app.globalData.right
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