// components/name/connect/index.ts
Component({
  properties: {
    user: Object,
  },
  data: {
    cls: "",
    label: ""
  },
  lifetimes: {
    attached () {
      this.setData({
        label: this.getConnectType(),
        cls: this.getConnectCls()
      })
    },
  },
  methods: {
    getConnectType () {
      switch (this.data.user?.connect_type) {
        case ("CLOSED"):
          return "不接受连接"
        case ("REQUIRE_APPROVE"):
          return "经同意后可获取手机/微信"
        case ("OPEN"):
          return "手机/微信可直接查看"
        return "-"
      }
    },
    getConnectCls () {
      switch (this.data.user?.connect_type) {
        case ("CLOSED"):
          return "bg-error"
        case ("REQUIRE_APPROVE"):
          return "bg-warn"
        case ("OPEN"):
          return "bg-primary"
        return "-"
      }
    }
  }
})
