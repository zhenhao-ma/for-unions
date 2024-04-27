import { get } from "../../utils/util"
const app = getApp();
// pages/dev/index.js
Component({
  properties: {

  },
  data: {

  },
  methods: {
    async getToken () {
      // Dev only, getToken
      const res = await get("/dev_only/get_token");
      app.globalData.isLogin = true
      app.globalData.userInfo = res.user
      wx.setStorageSync('accessToken', res.access_token)
    }
  }
})
