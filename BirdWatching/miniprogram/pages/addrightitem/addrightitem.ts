// pages/add/add.ts
import { wx_get_survey,wx_post_base64,wx_update_bird_survey} from '../../components/interface'

const checkapp=getApp()
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
    image:[],
    // 存储调查id
    bird_survey_id:'',
    record:[],
    // 上传视频
    src:"",        // 上传视频
    video:[],
    recorder: wx.getRecorderManager(),
    tmp:[],
    audio:'',
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
    miaoshu:'',
    shengjing:'',
    xixing:'',
    weather:'',
    temperature:'',
    tmpaudio:[],
    tmpimg:[],
    tmpvideo:[]
  },

  submit() {
    const fileManager = wx.getFileSystemManager();

    const soundPromise = this.data.tmp.map(au => {
      return new Promise((resolve, reject) => {
        const aubase64 = fileManager.readFileSync(au, 'base64');
        wx_post_base64({
          type: "sound",
          binary: aubase64
        }).then(res => {
          resolve(res.data);
        }).catch(error => {
          reject(error);
        });
      });
    });

    const imagesPromise = this.data.image.map((image) => {
      return wx_post_base64({
        type: "image",
        binary: image
      }).then((res) => {
        return res.data;
      });
    });
  
    const videosPromise = this.data.video.map(video => {
      return new Promise((resolve, reject) => {
        const videoase64 = fileManager.readFileSync(video, 'base64');
        wx_post_base64({
          type: "video",
          binary: videoase64
        }).then(res => {
          resolve(res.data);
          console.log(res.data);

        }).catch(error => {
          reject(error);
        });
      });
    });

Promise.all([Promise.all(soundPromise), Promise.all(imagesPromise), Promise.all(videosPromise)])
.then(([resolvedSoundPromises, resolvedImagePromises, resolvedVideoPromises]) => {
resolvedSoundPromises.forEach(res => {
  if (typeof res === "string") {
    this.data.tmpaudio.push(res);
  }
});

resolvedImagePromises.forEach(res => {
  if (typeof res === "string") {
    this.data.tmpimg.push(res);
  }
});

resolvedVideoPromises.forEach(res => {
  if (typeof res === "string") {
    this.data.tmpvideo.push(res);
  }
});

const data = {
  openid: checkapp.globalData.openid,
  token: checkapp.globalData.token,
  user_id: checkapp.globalData.userid,
  describe : this.data.miaoshu,
  habitat : this.data.shengjing,
  behavior : this.data.xixing,
  bird_survey_id :this.data.bird_survey_id,
  bird_info: [{
    sound: this.data.tmpaudio,
    image: this.data.tmpimg,
    videos: this.data.tmpvideo
  }]
  
};
console.log(data);
checkapp.globalCheck()
wx_update_bird_survey(data).then(res=>{
  console.log(res);
})
// 在这里可以访问其他操作的结果，然后返回data对象
return data;
// 在这里进行上传数据的操作
})
.catch(error => {
console.error('Error:', error);
});
},

  

  // 获取单个调查记录接口
  getBirdSurvey:function(){
    wx_get_survey({survey_id:this.data.bird_survey_id}).then(res=>{
      console.log(res);
      this.setData({
        record:res.data
      })
    })
  },

  getFileName (m:any) {
    m = m > 13 ? 13 : m;
    var num = new Date().getTime();
    return num.toString().substring(13 - m);
  },

  //提交按钮
  jumpToDetail() {
    var that = this
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
                      that.submit()
                 }
               })
               wx.switchTab({      
                url: '../../pages/home/home',
         }) 
                                                        
            }else{
               console.log('用户点击取消')
            }

        }
    })
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
        _this.data.video.push(_this.data.src)
      }
    })
  },
  getimg:function(e:any) {
    for(const item of e.detail){
     this.data.image.push(item.fileContent)
    }
  },
  delimg:function(e:any) {
    console.log(e.detail);
    this.data.image.splice(e.detail,1) 
  },
  

  // 录音
  //开始录音
  startClick() {
    var options = {
      format: 'mp3',
      duration: 10000,
    };
    this.data.recorder.start(options);

  },

  //结束录音
  stopClick() {
    this.data.recorder.stop();
  },

    //播放录音
playClick() {
  var audio = wx.createInnerAudioContext();
  audio.src = this.data.audio;
  audio.autoplay = true;
  console.log('播放录音');
},

  //描述
  miaoshu:function(e:any){
  this.setData({
    miaoshu: e.detail.value,
  })
  console.log(this.data.miaoshu);
},
// 生境
shengjing:function(e:any){
  this.setData({
    shengjing: e.detail.value,
  })
  console.log(this.data.shengjing);
},
// 习性
xixing:function(e:any){
  this.setData({
    xixing: e.detail.value,
  })
  console.log(this.data.xixing);
  
},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad:function(options) {
    this.setData({
      bird_survey_id:options.bird_survey_id
    })
    this.getBirdSurvey()
        //事件监听
      this.data.recorder.onStart(() => {
        console.info('开始录音');
      });
      this.data.recorder.onPause(() => {
        console.info('暂停录音');
      });
      //结束获取录取文件
      this.data.recorder.onStop((res) => {
        console.info('停止录音');
        console.info(res); //可以看到录音文件
        const au = res.tempFilePath        
        this.setData({
          audio: au
        });
        this.data.tmp.push(this.data.audio)
});
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
      checkapp.globalData.messageList[this.data.nav_type].Latitude = this.data.latitude
      checkapp.globalData.messageList[this.data.nav_type].Longitude = this.data.longitude
      
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