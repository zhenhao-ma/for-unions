declare type ObjectId = string
declare type Tag = string
declare type Datetime = string
interface DBModelBase {
  id: ObjectId
  created: Datetime
  updated: Datetime
  deleted: boolean
}