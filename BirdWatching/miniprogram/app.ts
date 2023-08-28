import { poskey, weatherkey } from "./components/config";
import { sgin, wx_get_all_birds,get_all_orders, check_info } from "./components/interface"
var amapFile = require('./utils/amap-wx.js');

var QQMapWX = require('./utils/qqmap-wx-jssdk.min.js');

var qqmapsdk = new QQMapWX({
  key: poskey    // 这里就是申请的key
});
var AmapFun = new amapFile.AMapWX({key: weatherkey});

// app.ts
App({
  globalData: {
    checkedList:[],
    messageList:[],
    userid:-1,
    openid:"",
    token:"",
    userInfo: {},
    latitude:0,
    longitude:0,
    address:'',
    temperature:0,
    weather:'',
    left:[],
    right:[],
    islogin:false,
    code:-1
  },
  getAllBird(){
    wx_get_all_birds().then(res=>{
      console.log(res);
      this.globalData.left=res
    })
  },
  getOrder:function(){
    get_all_orders().then(res=>{
        console.log(res);
        this.globalData.right=res
    })
  },

  getWeather(){
    var _this = this
    AmapFun.getWeather({
      success: function(data){
        //成功回调
        _this.globalData.temperature = Number(data.temperature.data)
        _this.globalData.weather = data.weather.data
      },
      fail: function(info){
        //失败回调
        console.log(info)
      }
    })
  },
  getAddressInfo() {
    var _this = this
    wx.getLocation({
      type: 'wgs84',
      success (res) {
        _this.globalData.latitude = res.latitude;
        _this.globalData.longitude = res.longitude
        qqmapsdk.reverseGeocoder({
          location:{
            latitude: res.latitude,
            longitude: res.longitude
          },
          success: (res: { result: any; address: string; }) => {
            _this.globalData.address = res.result.address
          },
        })
        }
     })
  },
  onLaunch() {
    //获取鸟库数据
    this.getOrder()
    this.getAllBird()
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    // 登录
    this.globalLongin()
    this.getAddressInfo()
    this.getWeather()
   
  },
  globalLongin(){
    const _this = this
    wx.login({
      success (res) {
        if (res.code) {
          //发起网络请求
          const data= {
            code: res.code
          }
          sgin(data).then(res => {
            _this.globalData.openid = res.openid,
            _this.globalData.token = res.session_key
            _this.globalData.userid = res.log
          })
        } else {
          console.log('登录失败！' + res.errMsg)
        }
      }
    })
  },
  // 判断登录状态

  globalCheck(){
    const _this = this
    wx.checkSession({
      success () {
        //session_key 未过期，并且在本生命周期一直有效
        console.log("未失效");
      },
      fail () {
        // session_key 已经失效，需要重新执行登录流程
        _this.globalLongin()//重新登录
      }
    })
  },
})