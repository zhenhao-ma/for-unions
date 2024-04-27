import { UNION_API } from "../../../api/index"
import { getPaginationData, paginate, PaginationData } from "../../../utils/pagination"

export type Data = PaginationData<IUnion>
const defaultData = getPaginationData<IUnion>()
Page<Data, any>({
  data: {
    ...defaultData,
    // loading: false,
    // unions: [],
    // page: 0,
    // pageSize: 10,
    // noMore: false
  },
  async onLoadPage (page: number) {
    paginate(this, UNION_API.UserList, page)
    // if (this.data.loading || this.data.noMore) return
    // this.setData({loading: true, page})
    // const unions = await UNION_API.UserList({
    //   skip: this.data.page * this.data.pageSize,
    //   limit: this.data.pageSize
    // })
    // this.setData({
    //   list: unions,
    //   loading: false,
    //   noMore: unions.length < this.data.pageSize
    // })
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