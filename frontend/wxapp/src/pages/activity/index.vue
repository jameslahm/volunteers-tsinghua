<template>
  <div>
    <view style="padding:15px;">
      <i-card :title="item.title" :extra="item.extra" :thumb="item.thumb">
        <view slot="content">{{item.content}}</view>
        <view slot="footer">{{item.footer}}</view>
      </i-card>
    </view>
  </div>
</template>

<script>

export default {
  data () {
    return {
      item: {}
    }
  },
  components: {},
  onLoad (options) {
    console.log('hello')
    this.item = {
      'title': '五道口支教',
      'extra': '队长：王澳',
      'thumb': 'https://avatars3.githubusercontent.com/u/43805318?s=460&v=4',
      'description': '我们是五道口支教团队',
      'content': '我们是五道口团队，啦啦啦啦',
      'footer': '10月5日 五道口',
      'time': '10月5日',
      'location': '五道口',
      'id': '123',
      'leader': '王澳'
    }
  },
  methods: {},
  created () {
    // let app = getApp()
  }
}
</script>

<style scoped>
</style>
