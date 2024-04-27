declare enum ReviewStatus {
  PENDING = 'PENDING',
  APPROVED = 'APPROVED',
  REJECTED = 'REJECTED'
}
interface IConnectCreate {
  to_user: ObjectId
  description?: string
}

interface IConnectReview {
  id: ObjectId
  status: ReviewStatus
}
interface IConnect extends DBModelBase {
  from_user: ObjectId
  to_user: ObjectId
  status: ReviewStatus
  description?: string
}