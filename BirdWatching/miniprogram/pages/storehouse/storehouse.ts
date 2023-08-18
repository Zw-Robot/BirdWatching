// pages/storehouse/storehouse.ts

import { get_all_birds, get_all_orders, wx_get_all_birds } from "../../components/interface";

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
      id:1,
      name:'雁形目 ANSERIFORMES1',
      twodata:[{
          'id':1,
          'name':'栗树鸭1',
          'lading':'Dendory',
          'english':'Leser',
          'subject':'鸭科'
      },
      {
          'id':2,
          'name':'栗树鸭2',
          'lading':'Dendory',
          'english':'Leser',
          'subject':'鸭科'
      }]
},
{
      id:2,
      name:'雁形目 ANSERIFORMES2',
      count:6,
      twodata:[{
          'id':3,
          'name':'栗树鸭1',
          'lading':'Dendory',
          'english':'Leser',
          'subject':'鸭科'
      },
      {
          'id':4,
          'name':'栗树鸭2',
          'lading':'Dendory',
          'english':'Leser',
          'subject':'鸭科'
      },
      {
        'id':5,
        'name':'栗树鸭3',
        'lading':'Dendory',
        'english':'Leser',
        'subject':'鸭科'
    }
    ]
},
{
      id:3,
      name:'雁形目 ANSERIFORMES3',
      count:12,
      twodata:[{
          'id':5,
          'name':'栗树鸭1',
          'lading':'Dendory',
          'english':'Leser',
          'subject':'鸭科'
      },{
          'id':6,
          'name':'栗树鸭2',
          'lading':'Dendory',
          'english':'Leser',
          'subject':'鸭科'
      }]
}],//鸟库数据
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
    // this.getcates();
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

  },
  })