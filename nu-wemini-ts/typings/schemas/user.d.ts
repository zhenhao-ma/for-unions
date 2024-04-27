declare enum UserRole  {
  ROOT = 'ROOT',
  ADMIN = 'ADMIN',
  USER = 'USER'
}
declare enum ConnectType {
  CLOSED = 'CLOSED',
  REQUIRE_APPROVE = 'REQUIRE_APPROVE',
  OPEN = 'OPEN'
}
interface IUserPreview extends DBModelBase {
  phone: Phone
  email?: Email
  country?: Country
  full_name: string
  role: UserRole
  unions: ObjectId[]
  tags: Tag[]
  avatar?: ObjectId
  description: string
  connect_type: ConnectType
}
interface IUserDetailed extends IUserPreview {
  phone: Phone
  email?: Email
}
interface IUserUpdate {
  full_name?: string
  country?: Country
  tags?: string[]
  avatar?: string
  description?: string
  connect_type?: ConnectType
}