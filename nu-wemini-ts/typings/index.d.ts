/// <reference path="./types/index.d.ts" />

interface IAppOption {
  globalData: {
    me?: IUserDetailed,
    isLogin?: boolean
  }
  userInfoReadyCallback?: WechatMiniprogram.GetUserInfoSuccessCallback,
}