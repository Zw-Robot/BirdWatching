import { wx_post_base64 } from "../components/interface"

export class BirdRecord{
  user_id:Number
  id:Number
  name:String
  Date:String
  Time:String
  Address: String
  Longitude:Number
  Latitude:Number
  Num:Number
  Count:Number
  images:AnyArray
  videos:AnyArray
  audios:AnyArray
  text:String
  tmpimg:AnyArray
  tmpvideo:AnyArray
  tmpaudio:AnyArray

  constructor(user_id:Number,id:Number,name:String,date:String,time:String,address:String='',num:Number=0,count:Number = 0,images:AnyArray=[],videos:AnyArray = [],audios:AnyArray = [],text:String = '',  longitude:Number = 0,
  latitude:Number = 0,tmpimg=[],tmpvideo=[],tmpaudio=[]){
    this.user_id = user_id
    this.id = id
    this.name = name
    this.Date = date
    this.Time = time
    this.Address = address
    this.Num = num
    this.Count = count
    this.images = images
    this.videos = videos
    this.audios = audios
    this.text = text 
    this.Longitude = longitude
    this.Latitude = latitude
    this.tmpaudio = tmpaudio
    this.tmpimg = tmpimg
    this.tmpvideo = tmpvideo

  }

  submit() {
    const fileManager = wx.getFileSystemManager();

    const soundPromise = this.audios.map(au => {
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

    const imagesPromise = this.images.map((image) => {
      return wx_post_base64({
        type: "image",
        binary: image
      }).then((res) => {
        return res.data;
      });
    });
  
    const videosPromise = this.videos.map(video => {
      return new Promise((resolve, reject) => {
        const videoase64 = fileManager.readFileSync(video, 'base64');
        wx_post_base64({
          type: "video",
          binary: videoase64
        }).then(res => {
          resolve(res.data);
        }).catch(error => {
          reject(error);
        });
      });
    });

    Promise.all(soundPromise)
      .then(resolvedSoundPromises => {
        resolvedSoundPromises.forEach(res => {
          if (typeof res === "string") {
            this.tmpaudio.push(res);
          }
        });
      })
      .catch(error => {
        console.error('Error:', error);
      });

    Promise.all(imagesPromise)
      .then(resolvedImagePromises => {
        resolvedImagePromises.forEach(res => {
          if (typeof res === "string") {
            this.tmpimg.push(res);
          }
        });
      })
      .catch(error => {
        console.error('Error:', error);
      });

    Promise.all(videosPromise)
      .then(resolvedVideoPromises => {
        resolvedVideoPromises.forEach(res => {
          if (typeof res === "string") {
            this.tmpvideo.push(res);
          }
        });
      })
      .catch(error => {
        console.error('Error:', error);
      });

    Promise.all([soundPromise,imagesPromise, videosPromise])
    .then(res => {
      const data = {
        user_id: this.user_id,
        bird_id: 4,
        record_time: `${this.Date} ${this.Time}`,
        record_location: this.Address,
        longitude: this.Longitude,
        latitude: this.Latitude,
        weather: "Sunny",
        temperature: 26,
        record_describe: this.text,
        bird_infos: [{
          sound: this.tmpaudio,
          image: this.tmpimg,
          videos: this.tmpvideo
        }]
      };
      console.log(data);
      
      // 在这里可以访问其他操作的结果，然后返回data对象
      return data;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }
}

