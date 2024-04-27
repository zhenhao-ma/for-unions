import { USER_API } from "../../api/user"
import { UNION_API } from "../../api/union"
import { isDef } from "../../utils/util"

const app = getApp<IAppOption>()

// pages/union/index.ts
export type Data = {
  loading: boolean
  union?: IUnion
  users: IUserPreview[]
  page: number,
  pageSize: number
}

Page<Data, any>({
  data: {
    loading: false,
    union: null,
    users: [],
    page: 0,
    pageSize: 10,
    isAdmin: false
  },
  async onLoad(options: { id: string }) {
    let id = decodeURIComponent(options.id)
    
    this.setData({loading: true, page: 0})
    const union = await UNION_API.PublicGet({
      id
    })
    const users = await USER_API.PublicList({
      union_id: union.id,
      skip: this.data.page * this.data.pageSize,
      limit: this.data.pageSize
    })
    this.setData({
      union,
      users,
      loading: false,
      isAdmin: this.getIsAdmin(union)
    })
  },
  onReady() {

  },
  onShow() {

  },
  onHide() {

  },
  onUnload() {

  },
  onPullDownRefresh() {

  },
  async onReachBottom() {
    if (this.data.loading) return
    const page = this.data.page + 1
    this.setData({loading: true, page})
    const users = await USER_API.PublicList({
      union_id: this.data.union.id,
      skip: page * this.data.pageSize,
      limit: this.data.pageSize
    })
    this.setData({loading: false, users: [...this.data.users, ...users]})
  },
  onShareAppMessage() {

  },
  getIsAdmin (union: IUnion) {
    console.log("app.globalData.me: ", app.globalData.me)
    console.log("union: ", union)
    console.log("this.union?.admins: ", union?.admins)
    if (isDef(app.globalData.me?.id) && isDef(union?.admins)) {
      return union.admins.includes(app.globalData.me?.id as any)
    }
    return false
  }
})