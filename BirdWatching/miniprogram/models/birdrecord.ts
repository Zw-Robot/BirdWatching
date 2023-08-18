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

  constructor(user_id:Number,id:Number,name:String,date:String,time:String,address:String='',num:Number=0,count:Number = 0,images:AnyArray=[],videos:AnyArray = [],audios:AnyArray = [],text:String = '',  longitude:Number = 0,
  latitude:Number = 0,){
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
  }

  submit() {
    var data = {
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
          sound: this.audios,
          image: this.images,
          videos: this.videos
      }]
    }
    console.log(data);
    
    return data
  }
}

