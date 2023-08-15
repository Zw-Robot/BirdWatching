export class BirdRecord{
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

  constructor(id:Number,name:String,date:String,time:String,address:String='',num:Number=0,count:Number = 0,images:AnyArray=[],videos:AnyArray = [],audios:AnyArray = [],text:String = '',  longitude:Number = 0,
  latitude:Number = 0,){
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
}

