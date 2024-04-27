// pages/me/editor/index.ts
import { USER_API } from '../../api/index'
import {config} from '../../config'
const app = getApp<IAppOption>()
export type Data = {
  full_name: string;
  phone: string;
  connect_type: ConnectType;
  email: string;
  description: string;
  country: Country;
  countryOption: Option<Country>;
  countries: Option<Country>[];
  tags: string[]
}
Component<Data, any, any>({
  properties: {
    user: {
      type: Object
    }
  },
  lifetimes: {
    attached: function () {
      console.log("Attached: ", this.properties.user)
      this.setData({
        full_name: this.properties.user?.full_name ?? "",
        phone: this.properties.user?.phone ?? "",
        connect_type: this.properties.user?.connect_type,
        email: this.properties.user?.email,
        country: this.properties.user?.country,
        tags: this.properties.user?.tags ?? [],
        description: this.properties.user?.description ?? ""
      })
    },
  },
  data: {
    full_name: "",
    phone: "",
    connect_type: "REQUIRE_APPROVE" as ConnectType.REQUIRE_APPROVE, // default
    email: "",
    country: "US" as Country.US,
    countryOption: config.COUNTRIES.filter(opt => opt.id === "US")[0],
    countries: config.COUNTRIES,
    description: "",
    tags: []
  },
  methods: {
    pickCountry (e: any) {
      const i = parseInt(e.detail.value);
      const countryOption = config.COUNTRIES[i]
      this.setData({
        country: countryOption.id,
        countryOption
      })
    },
    async onSave () {
      const res = await USER_API.UserUpdate({
        full_name: this.data.full_name,
        connect_type: this.data.connect_type,
        country: this.data.country,
        tags: this.data.tags,
        description: this.data.description
      })
      app.globalData.me = res
      wx.navigateBack()
    },
    setTags (e: any) {
      this.setData({
        tags: e.detail
      })
    }
  }
})
