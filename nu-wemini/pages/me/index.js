const app = getApp();
Component({
  properties: {
  },
  data: {
    isLogin: false,
    userInfo: null
  },
  onShow: () => {
    // init global data into local component
    this.setData({
      isLogin: app.globalData.isLogin,
      userInfo: app.globalData.userInfo
    })
  },
  methods: {
  }
})
