interface IUnionCreate {
  phone: Phone
  email: Email
  name: string
  description: string
}
interface IUnionUpdate {
  phone: Phone
  email: Email
  name: string
  description: string
}
interface IUnion extends DBModelBase {
  admins: ObjectId[]
  logo?: ObjectId
}