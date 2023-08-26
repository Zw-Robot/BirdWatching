export class BirdRecord{
  user_id:Number
  survey_name = String
  survey_desc = String
  survey_time = String
  survey_location = String
  describe = String
  habitat = String
  behavior = String

  constructor(
    user_id:Number,
    survey_name = String,
    survey_desc = String,
    survey_time = String,
    survey_location = String,
    describe = String,
    habitat = String,
    behavior = String
  ){
    this.user_id = user_id
    this.survey_name = survey_name
    this.survey_desc = survey_desc
    this.survey_time = survey_time
    this.survey_location = survey_location
    this.describe = describe
    this.habitat = habitat
    this.behavior = behavior
  }
}