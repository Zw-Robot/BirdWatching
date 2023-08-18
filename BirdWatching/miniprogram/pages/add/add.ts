// pages/add/add.ts
import { appname, poskey } from "../../components/config";
import { create_bird_record, create_bird_survey } from "../../components/interface";
const checkapp=getApp()
const recorder = wx.getRecorderManager();
let currentDate = new Date();

let hours = currentDate.getHours().toString().padStart(2, '0');
let minutes = currentDate.getMinutes().toString().padStart(2, '0');

let currentTime = hours + ':' + minutes;

let year = currentDate.getFullYear().toString();
let month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
let day = currentDate.getDate().toString().padStart(2, '0');

let currentDateString = year + '-' + month + '-' + day;
const chooseLocation = requirePlugin('chooseLocation');
Page({

  /**
   * 页面的初始数据
   */
  data:{
    // 上传视频
    src: "",        // 上传视频
    time:currentTime,
    date:currentDateString,
    checkedList:['1',checkapp.globalData.checkedList],
    messageList:[checkapp.globalData.messageList],
    //灰色顶部
    navList:['待添加鸟类',checkapp.globalData.checkedList],
    nav_type:0,//默认选中第一个
    mav_type:0,
    isFixed:false,//是否吸顶
    navTop:0,//nav菜单激励顶部距离
    address:'',
    longitude:0.0,
    latitude:0.0,
    count:0,//数量
    num:0,//人数,
    images:[],
    videos:[],
    audios:[],
    text:''
  },

  //灰色顶部
  changeType(e:any){
    let{index}=e.currentTarget.dataset;
    if(this.data.nav_type==index||index==undefined) return;
    console.log(checkapp.globalData.messageList);
    this.setData({
      nav_type:index,
      date:checkapp.globalData.messageList[index].Date,
      time:checkapp.globalData.messageList[index].Time,
      address:checkapp.globalData.messageList[index].Address,
      longitude:checkapp.globalData.messageList[index].Longitude,
      latitude:checkapp.globalData.messageList[index].Latitude,
      count:checkapp.globalData.messageList[index].Count,
      num:checkapp.globalData.messageList[index].Num,
      images:checkapp.globalData.messageList[index].images,
      videos:checkapp.globalData.messageList[index].videos,
      audios:checkapp.globalData.messageList[index].audios,
      text:checkapp.globalData.messageList[index].text,
    })
    console.log(this.data.nav_type);
  
    if(this.data.isFixed){
      wx.pageScrollTo({
        selector:'#content',
        duration:0.5
      })
    }
  },

  //提交按钮
  jumpToDetail() {
    // create_bird_survey({parmas:this.data.messageList}).then(res=>{
    //   console.log(res);
      
    // })
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
                      for(const item of checkapp.globalData.messageList){
                        var data = item.submit()
                        console.log(data);
                        
                        create_bird_record(data).then(res=>{
                          console.log(res);
                          
                        })
                      }
                      checkapp.globalData.messageList = []
                 }
               })
                                                        
            }else{
               console.log('用户点击取消')
            }

        }
    })
},

  // 添加日期
  bindDateChange: function(e:any) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      date: e.detail.value,
    })
    checkapp.globalData.messageList[this.data.nav_type].Date=this.data.date
    console.log(checkapp.globalData.messageList);
  },
  //添加时间
  bindTimeChange: function(e:any) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      time: e.detail.value
    })
    checkapp.globalData.messageList[this.data.nav_type].Time=this.data.time
    console.log(checkapp.globalData.messageList);
  },
  ChoosePoint:function()
  { 
    const key = poskey
    const referer = appname
    const category = '';
    const location = JSON.stringify({
      latitude: 39.89631551,
      longitude: 116.323459711
    });
    wx.navigateTo({
      url: 'plugin://chooseLocation/index?key=' + key + '&referer=' + referer + '&location=' + location + '&category=' + category
    });
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
      count:this.data.count+1
    })
    checkapp.globalData.messageList[this.data.nav_type].Count=this.data.count
  },
  //减少数量
  subtract:function(){
    this.setData({
      count:this.data.count<=0? 0:this.data.count-1
    })
    checkapp.globalData.messageList[this.data.nav_type].Count=this.data.count
  },
  //添加人数
  add:function(){
    this.setData({
      num:this.data.num+1
    })
    checkapp.globalData.messageList[this.data.nav_type].Num=this.data.num
  },
  //减少人数
  subtractnumber:function(){
    this.setData({
      num:this.data.num<=0? 0:this.data.num-1,
    })
    checkapp.globalData.messageList[this.data.nav_type].Num=this.data.num
  },

  // 上传视频
  /**
   * 选择视频
   */
  chooseVideo: function() {
    var _this = this;
    wx.chooseVideo({
      success: function(res) {
        _this.setData({
          src: res.tempFilePath,
        })
        wx.getFileSystemManager().readFile({
      
          filePath: _this.data.src,
          encoding: 'base64',
          success: function (res) {
            checkapp.globalData.messageList[_this.data.nav_type].videos.push(res.data)
          }
          })
      }
      
    })
    console.log( checkapp.globalData.messageList);
    
  },
  getimg:function(e:any) {
    for(const item of e.detail){
      checkapp.globalData.messageList[this.data.nav_type].images.push(item.fileContent)
    }
    console.log(checkapp.globalData.messageList);
  },
  delimg:function(e:any) {
    console.log(e.detail);
    checkapp.globalData.messageList[this.data.nav_type].images.splice(e.detail,1) 
    console.log(checkapp.globalData.messageList);
  },
  /**
   * 上传视频 目前后台限制最大100M, 以后如果视频太大可以选择视频的时候进行压缩
   */
  uploadvideo: function() {
    var src = this.data.src;
    console.log(src);
    
    wx.uploadFile({
      url: '',
      // methid: 'POST',           // 可用可不用
      filePath: src,
      name: 'files',              // 服务器定义key字段名称
      header: checkapp.globalData.header,
      success: function() {
        console.log('视频上传成功')
      },
      fail: function() {
        console.log('接口调用失败')
      }
    })
  },

  // 录音
  //开始录音
  startClick() {
    var options = {
      format: 'mp3',
      duration: 10000,
    };
    recorder.start(options);
    
  },

  //结束录音
  stopClick() {
    recorder.stop();
    
  },

    //播放录音
playClick() {
  var audio = wx.createInnerAudioContext();
  audio.src = this.data.file.tempFilePath;
  audio.autoplay = true;
  console.log('播放录音');
},

  //备注
searchInput:function(e:any){

  this.setData({
    text: e.detail.value,
  })
  checkapp.globalData.messageList[this.data.nav_type].text = this.data.text
  console.log(checkapp.globalData.messageList);

},

    //上传录音
// uploadClick() {
//   var file = this.data.file;
//   //后端使用相同的上传处理 common/upload 或者自己写一个
//   wx.uploadFile({
//     filePath: file.tempFilePath,
//     name: '音频文件',
//     url: url.getDomain() + '/common/upload',
//     formData: {
//       backinfo: JSON.stringify({
//         handleType: 0
//       })
//     },
//     success: res => {
//       var data=JSON.parse(res.data);
//       console.info(data);
//       console.info('上传成功');
//     }
//   })
// },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad:function() {
    this.setData({
      checkedList:checkapp.globalData.checkedList
    })
    this.setData({
      navList:checkapp.globalData.checkedList
    })
    this.setData({
      messageList:checkapp.globalData.messageList
    })

    var _this = this;
    //事件监听
    recorder.onStart(() => {
      console.info('开始录音');
    });
    recorder.onPause(() => {
      console.info('暂停录音');
    });
    //结束获取录取文件
    recorder.onStop((res) => {
      console.info('停止录音');
      console.info(res); //可以看到录音文件
      _this.setData({
        file: res
      });
    });

    //获取定位
    wx.getLocation({
      isHighAccuracy:true,
      success(res){
        console.log(res,"定位后获取信息");
      }
    })
  },
  togglePopup(e:any) {
    this.setData({
        visibility: e.currentTarget.dataset.type
    })
},
getValue(e:any) {
  console.log(e.detail);
  this.setData({
      dateTime: e.detail,
      visibility: false,
  })
},

//删除
deletebird(e:any) {
  // 获取图片索引
  var navList = this.data.navList;
  let index = e.currentTarget.dataset.index  // 获取数据的索引
  navList.splice(index,1)
  this.setData({
    navList: navList,
    checkedList: navList,
    mav_type:index,
  })
  checkapp.globalData.messageList.pop(index,1)
  console.log(checkapp.globalData.messageList);
  
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
    
    const loc = chooseLocation.getLocation();
    try{
      this.setData({
        address: loc.address,
        latitude: loc.latitude,
        longitude: loc.longitude,
      });
      checkapp.globalData.messageList[this.data.nav_type].Address = this.data.address
      checkapp.globalData.messageList[this.data.nav_type].latitude = this.data.latitude
      checkapp.globalData.messageList[this.data.nav_type].longitude = this.data.longitude
    }
    catch{
      this.setData({
        address: "",
        latitude: 0.0,
        longitude: 0.0,
      });
    }

    this.setData({
      checkedList:checkapp.globalData.checkedList
    })
    this.setData({
      navList:checkapp.globalData.checkedList
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
    chooseLocation.setLocation(null);
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