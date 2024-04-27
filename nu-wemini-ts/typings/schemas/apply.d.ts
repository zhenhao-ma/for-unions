interface IApplyCreate {
  union: ObjectId
  description?: string
}
interface IApplyReview {
  apply_id: ObjectId
  status: ReviewStatus
  rejected_reason?: string
}
interface IApply extends DBModelBase {
  union: ObjectId
  union_name?: string
  applicant: ObjectId
  applicant_name?: string
  applicant_phone?: string
  status: ReviewStatus
  handler?: ObjectId
  description?: string
  rejected_reason?: string
}