export type PaginationData<T> = {
  loading: boolean
  list: T[],
  page: number,
  pageSize: number,
  noMore: boolean
}
export type ObjData<T> = {
  obj: T,
  loading: boolean
}
export function getPaginationData<T>() {
  return {
    loading: false,
    list: [] as T[],
    page: 0,
    pageSize: 10,
    noMore: false
  }
}
export function getObjData<T>() {
  return {
    loading: false,
    obj: undefined
  }
}
export async function paginate<T>(this_: any, request_: (params: { skip: number, limit: number }) => Promise<T[]>, page: number) {
  if (this_.data.loading || this_.data.noMore) return
  this_.setData({ loading: true, page })
  const newList = await request_({
    skip: page * this_.data.pageSize,
    limit: this_.data.pageSize
  })
  this_.setData({
    list: [...this_.data.list, ...newList],
    loading: false,
    noMore: newList.length < this_.data.pageSize
  })
}
export async function getObj<T>(this_: any, request_: (params: { id: string }) => Promise<T | undefined>, id: string) {
  if (this_.data.loading) return
  this_.setData({ loading: true })
  const objData = await request_({
    id
  })
  this_.setData({
    loading: false,
    objData
  })
}