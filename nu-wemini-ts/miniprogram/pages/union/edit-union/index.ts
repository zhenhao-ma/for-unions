import { UNION_API } from "../../../api/index"
import { getObj, getObjData } from "../../../utils/pagination"

const defaultData = getObjData()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    ...defaultData
  },
  onLoad(options: { id: string }) {
    let id = decodeURIComponent(options.id)
    getObj(this, UNION_API.PublicGet, id)
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

  }
})