// index.ts
// 获取应用实例
const app = getApp<IAppOption>()
export type Data = {
  me?: IUserDetailed
  isLogin?: boolean
}
Page<Data, any>({
  data: {
    me: undefined,
    isLogin: false
  },
  bindViewTap() {
    wx.navigateTo({
      url: '../logs/logs',
    })
  },
  onLoad() {
  },
  
})
