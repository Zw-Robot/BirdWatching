import { sgin } from "./components/interface"

// app.ts
App({
  globalData: {
    checkedList:[],
    messageList:[],
    userid:-1,
    openid:"",
    token:""
  },
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    // 登录
    this.globalLongin()
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
            console.log(res);
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