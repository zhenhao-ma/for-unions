import { DEV_ONLY_API } from "../../api/dev_only"
const app = getApp<IAppOption>()
export type Data = {
    phone: string
}
// pages/dev/index.ts
Page<Data, any>({
  data: {
    phone: "12345678910"
  },
  onLoad() {

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

  onReachBottom() {

  },
  onShareAppMessage() {

  },
  async getToken () {
    // Dev only, getToken
    try {
        const res = await DEV_ONLY_API.Register(this.data.phone);
        app.globalData.isLogin = true
        app.globalData.me = res.user
        wx.setStorageSync('accessToken', res.access_token)
    } catch (e) {

    }
  },
  async generateRandomApplies () {
    const status = await DEV_ONLY_API.GenerateRandomApplies();
    if (status.status === true) {
      console.log("created")
    } else {
      console.error(status)
    }
  }
})