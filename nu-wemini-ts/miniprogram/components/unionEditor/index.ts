import { UNION_API } from "../../api/index"
import { isDef } from "../../utils/util"
export type Data = {
  phone: string
  email: string
  name: string
  description: string
}

// components/unionEditor/index.ts
Component<Data, any, any>({
  /**
   * 组件的属性列表
   */
  properties: {
    union: {
      type: Object,
      value: null
    }
  },
  data: {
    phone: "",
    email: "",
    name: "",
    description: ""
  },
  lifetimes: {
    attached () {
      this.setData({
        phone: this.properties.union?.phone ?? "",
        email: this.properties.union?.email ?? "",
        name: this.properties.union?.name ?? "",
        description: this.properties.union?.description ?? ""
      })
    }
  },
  methods: {
    async onSave () {
      if (isDef(this.properties.union?.id)) {
        const res = await UNION_API.UserUpdate(this.properties.union?.id, {
          phone: this.data.phone,
          email: this.data.email,
          name: this.data.name,
          description: this.data.description
        })
        console.log("update: ", res)
      } else {
        const res = await UNION_API.UserCreate({
          phone: this.data.phone,
          email: this.data.email,
          name: this.data.name,
          description: this.data.description
        })
        console.log("create: ", res)
      }
    }
  }
})
