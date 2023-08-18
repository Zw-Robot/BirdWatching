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

import { get_all_birds, get_all_orders, wx_get_all_birds } from "../../components/interface";

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
    rightMenuList:[
      {
        id:1,
        name:'雁1'
      },
      {
        id:2,
        name:'雁2'
      },
      {
        id:3,
        name:'雁3'
      },
      {
        id:4,
        name:'雁4'
      }
    ],//边侧栏数据
    leftMenuList:[{
      name:'雁形目 ANSERIFORMES1',
      twodata:[{
          id:1,
          value:'栗树鸭1',
          nameitem:'栗树鸭1',
          lading:'Dendory',
          english:'Leser',
          subject:'鸭科',
      },
      {
          id:2,
          value:'栗树鸭2',
          nameitem:'栗树鸭2',
          lading:'Dendory',
          english:'Leser',
          subject:'鸭科',
      }]
},
{
      name:'雁形目 ANSERIFORMES2',
      twodata:[{
          id:3,
          value:'栗树鸭3',
          nameitem:'栗树鸭3',
          lading:'Dendory',
          english:'Leser',
          subject:'鸭科',
      },
      {
          id:4,
          value:'栗树鸭4',
          nameitem:'栗树鸭4',
          lading:'Dendory',
          english:'Leser',
          subject:'鸭科',
      },
      {
          id:5,
          value:'栗树鸭5',
          nameitem:'栗树鸭5',
          lading:'Dendory',
          english:'Leser',
          subject:'鸭科',
    }
    ]
},
{
      name:'雁形目 ANSERIFORMES3',
      twodata:[{
          id:6,
          value:'栗树鸭6',
          nameitem:'栗树鸭6',
          lading:'Dendory',
          english:'Leser',
          subject:'鸭科',
      },{
          id:7,
          value:'栗树鸭7',
          nameitem:'栗树鸭7',
          lading:'Dendory',
          english:'Leser',
          subject:'鸭科',
      }]
}],//鸟库数据
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
  //获取被选中的复选框的值
  app.globalData.checkedList = e.detail.value;
  console.log(app.globalData.checkedList);

  app.globalData.messageList = []
  for(const val of e.detail.value){
    const id = app.globalData.messageList.length 
    console.log(val)
    const br:BirdRecord = new BirdRecord(id,val,currentDateString,currentTime,)
    app.globalData.messageList.push(br)
  }
  console.log(app.globalData.messageList);
  
  
},

getAllBirds:function(){
  wx_get_all_birds().then(res=>{
    this.setData({
      leftMenuList:res
    })
    console.log(res);
    
  })
},

getOrder:function(){
  get_all_orders().then(res=>{
    this.setData({
      rightMenuList:res
    })
  })
},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    this.getAllBirds();
    this.getOrder()
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