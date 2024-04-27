import { USER_API } from "./api/index"
import { isDef } from "./utils/util"

// app.ts
App<IAppOption>({
  globalData: {
    me: undefined,
    isLogin: false
  },
  async onLaunch() {
    try {
      var value = wx.getStorageSync('accessToken')
      if (value) {
        // try to login
        const userRes = await USER_API.UserGetSelf()
        console.log("userRes: ", userRes)
        if (isDef(userRes?.id)) {
          this.globalData.isLogin = true
          this.globalData.me = userRes
        }
      }
    } catch (e) {
      // Do something when catch error
    }
  },
})