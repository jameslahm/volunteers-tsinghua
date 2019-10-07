<template>
  <div>
    <i-panel title="申请创建">
      <view style="padding:15px;">
        <i-card @click='bindClick(item)' v-for="(item,index) in createdItems" :key=index :title="item.title" :extra="item.extra" :thumb="item.thumb" i-class="card-thumb">
          <view slot="content">{{item.description}}</view>
          <view slot="footer">{{item.footer}}</view>
        </i-card>
      </view>
    </i-panel>
    <i-panel title="申请加入">
      <view style="padding:15px;">
        <i-card @click='bindClick(item)' v-for="(item,index) in applyedItems" :key=index :title="item.title" :extra="item.extra" :thumb="item.thumb" i-class="card-thumb">
          <view slot="content">{{item.description}}</view>
          <view slot="footer">{{item.footer}}</view>
        </i-card>
      </view>
    </i-panel>
  </div>
</template>

<script>

export default {
  data () {
    return {
      createdItems: [
        {
          'title': '五道口支教',
          'extra': '队长：王澳',
          'thumb': 'https://avatars3.githubusercontent.com/u/43805318?s=460&v=4',
          'description': '我们是五道口支教团队',
          'footer': '10月5日 五道口',
          'time': '10月5日',
          'location': '五道口',
          'id': '123'
        }
      ],
      applyedItems: [
        {
          'title': '五道口支教',
          'extra': '队长：王澳',
          'thumb': 'https://avatars3.githubusercontent.com/u/43805318?s=460&v=4',
          'description': '我们是五道口支教团队',
          'footer': '10月5日 五道口',
          'time': '10月5日',
          'location': '五道口',
          'id': '123'
        }
      ],
      openid: 123
    }
  },

  components: {},

  methods: {
    'bindClick': function (item) {
      wx.navigateTo({ url: '/pages/activity/main?id=' + item.id })
    }
  },
  onLoad (options) {
    wx.login({
      success: res => {
        console.log(res)
        this.openid = 123
      },
      fail: () => { console.log('error') },
      complete: () => {}
    })
  },
  created () {
    // let app = getApp()
  }
}
</script>

<style>
.card-thumb image {
  border-radius: 50%;
}
</style>
