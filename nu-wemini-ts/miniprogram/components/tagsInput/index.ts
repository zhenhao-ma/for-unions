// components/tagsInput/index.ts
export type Data = {
  
}
export type Properties = {
  tags: string[]
}
Component<Data, any, any, any>({
  properties: {
    tags: Object
  },

  data: {
    newTag: "",
    focused: false
  },
  lifetimes: {
    attached () {
      console.log("tags: ", this.data.tags)
    }
  },
  methods: {
    sanitizeTag (t: string) {
      return (t ?? "").trim()
    },
    onAdd () {
      const t = this.sanitizeTag(this.data.newTag)
      const tags = this.data.tags ?? [];
      if (t.length > 0 && !tags.includes(t)) {
        console.log("this.setTags: ", this.properties.setTags)
        let newTags = [...tags, t];
        this.triggerEvent('settags', newTags);
        this.setData({
          "tags": newTags
        })
      }
    },
    onInputFocus () {
      console.log("input focus")
      this.setData({
        focused: true
      })
    },
    onInputBlur () {
      console.log("onInputBlur")
      this.onAdd();
      this.setData({
        newTag: "",
        focused: false
      })
    }
  }
})
