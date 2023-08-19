// components/attendimage/attendimage.ts
// const app = getApp();
Component({
  properties: {
    fileList: {
      type: Array
    },
    prevent: {
      type: Boolean,
      value: false
    }
  },
  data: {
    fileChildList: []
  },
  observers:{
    'fileList':function (newval) {
      console.log(newval);
      this.setData({
        fileChildList:newval
      })
    }
  },
  ready() {},
  methods: {
    // 点击加号进入手机相册，并进行图片选择
    _addImg() {
      let _this = this;
      // 此方法为微信小程序自带api 详情访问https://developers.weixin.qq.com/miniprogram/dev/api/media/image/wx.chooseImage.html
      wx.chooseImage({
        count: 5,
        success(res) {
          //此处会返回图片暂存路径和文件大小
          const data = res.tempFiles;
          _this.setFile(data)
        }
      })
    },

    setFile (data:any) {
      // 将wx.chooseImage返回的数据进行扩展
      data.map((item:any, index:any) => {
        // 通过路径截取文件后缀名
        const fileFormat = item.path.substring(item.path.lastIndexOf(".") + 1, item.path.length);
        // wx.getFileSystemManager()小程序文件管理器api，可以将通过文件路径将其转换成64编码
        const fileManager = wx.getFileSystemManager();
        const base64 = fileManager.readFileSync(item.path, 'base64');
        item.fileContent = base64;
        item.fileSize = item.size;
        // 通过时间获取随机13位随机数并且拼接文件后缀进行文件命名
        item.fileName = this.getFileName(13) + '.' + fileFormat;
        // 此处操作是用来进行选中图片显示的，只有这样拼接才能显示base64编码的路径
        item.path = `data:image/${fileFormat};base64,${base64}`;;
      })
      this.setData({ 
        fileChildList: this.data.fileChildList.concat(data)
      });
      // 此处操作是用来将获取到的文件数据传递给父组件进行文件上传
      this.triggerEvent('imageChange', this.data.fileChildList)
    },
    // 随机生成文件名
    getFileName (m:any) {
      m = m > 13 ? 13 : m;
      var num = new Date().getTime();
      return num.toString().substring(13 - m);
    },
    //点击进行图片删除
    _onDelTab(e:any) {
      // 获取图片索引
      let idx = e.currentTarget.dataset.idx;
      let delFile = this.data.fileChildList[idx];
      console.log(delFile);
      this.data.fileChildList.splice(idx, 1);
      this.setData({
        fileChildList: this.data.fileChildList
      })
      this.triggerEvent('imageDel', idx);
    }
  }
})