import { UNION_API } from "../../../api/index"
import { getPaginationData, paginate, PaginationData } from "../../../utils/pagination"

export type Data = PaginationData<IApply>
const defaultData = getPaginationData<IApply>()
Page<Data, any>({
  data: {
    ...defaultData,
  },
  async onLoadPage (page: number) {
    paginate(this, UNION_API.UserListApply, page)
  },
  async onLoad() {
    this.onLoadPage(0)
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

  async onReachBottom() {
    this.onLoadPage(this.data.page + 1)
  },

  onShareAppMessage() {

  }
})