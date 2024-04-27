import { USER_API } from "../../api/index"
import { isDef } from "../../utils/util"
import { config } from '../../config'

// pages/me/index.ts
const app = getApp<IAppOption>()
export type Data = {
  me?: IUserDetailed
  isLogin: boolean
  phone?: string
  phoneSecret?: string
  countries: Option<Country>[]
}
Page<Data, any>({
  data: {
    me: undefined,
    isLogin: false,
    phone: undefined,
    phoneSecret: undefined,
    countries: config.COUNTRIES
  },
  onLoad() {
  },
  onReady() {
  },
  onShow() {
    this.setData({
      isLogin: app.globalData.isLogin,
      me: app.globalData.me
    })
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
  async getPhoneNumber(e: unknown) {
    try {
      // get phone number from wechat api
      const res = await USER_API.PublicWeminiGetPhone((e as any).detail.code)
      const data = { phone: res.phone, phoneSecret: res.secret }
      this.setData(data);
      if (isDef(res)) {
        this.wxLogin(data)
      }
    } catch (error) {
      console.log(error)
    }
  },

  logout() {
    var app = getApp();
    app.globalData.isLogin = true
    this.setData({
      isLogin: false,
      me: undefined
    })
    wx.removeStorageSync('accessToken')
  },

  wxLogin({ phone, phoneSecret }: { phone: string, phoneSecret: string }) {
    wx.login({
      success: async (loginRes) => {
        if (loginRes.code) {
          // exchange user data with js code
          const params = {
            js_code: loginRes.code,
            phone: phone,
            secret: phoneSecret,
          }
          const res = await USER_API.PublicWeminiLogin(params)
          if (res) {
            app.globalData.isLogin = true
            app.globalData.me = res.user
            wx.setStorageSync('accessToken', res.access_token)
            this.setData({
              isLogin: true,
              me: res.user
            })
          }
        } else {
          console.log('系统出错了，登录失败')
        }
      }
    })
  }
})