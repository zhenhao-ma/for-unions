import { get, isDef } from '../../utils/util.js'
const app = getApp()

Page({
  data: {
    phone: null,
    phoneSecret: null
  },
  bindViewTap() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad() {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
  },
  async getPhoneNumber(e) {
    try {
      // get phone number from wechat api
      const res = await get('/user/public/wemini/get_phone', { wx_code: e.detail.code })
      const data = { phone: res.phone, phoneSecret: res.secret }
      this.setData(data);
      if (isDef(res)) {
        this.wxLogin(data)
      }
    } catch (error) {
      console.log(error)
    }
  },

  loginOut() {
    var app = getApp();
    app.globalData.isLogin = true
    this.setData({
      isLogin: false
    })
    wx.removeStorageSync('accessToken')
  },
  
  wxLogin({ phone, phoneSecret }) {
    wx.login({
      success: async (loginRes) => {
        if (loginRes.code) {
          // exchange user data with js code
          const params = {
            js_code: loginRes.code,
            phone: phone,
            secret: phoneSecret,
          }
          const res = await get('/user/public/wemini/login', params)
          if (res) {
            app.globalData.isLogin = true
            app.globalData.userInfo = res.user
            wx.setStorageSync('accessToken', res.access_token)
          }
        } else {
          console.log('登录失败！' + res.errMsg)
        }
      }
    })
  }
})
