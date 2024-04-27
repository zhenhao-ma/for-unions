// pages/me/my-settings/index.ts
const app = getApp<IAppOption>()
export type Data = {
  me?: IUserDetailed
}
Page<Data, any>({
  data: {
    me: null
  },
  onShow () {
    this.setData({
      me: app.globalData.me
    })
  }
})