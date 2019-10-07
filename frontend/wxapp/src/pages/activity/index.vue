<template>
  <div>
    <view style="padding:15px;">
      <i-card :title="item.title" :extra="item.extra" :thumb="item.thumb" i-class="card-thumb">
        <view slot="content">
          <i-panel :title="item.description">
            <view style="padding:15px;">
              {{item.content}}
            </view>
          </i-panel>
        </view>
        <view slot="footer">
          <i-panel title="团队成员" hide-border hide-top>
            <i-avatar v-for="(member,index) in item.members" :key=index :src="member.avatar" size=large style="padding:8px;">
            </i-avatar>
          </i-panel>
        </view>
      </i-card>
      <view v-if="openid===item.leader" style="display:flex;justify-content:center;">
          <i-button @click="manageActivity(item)" type="primary" inline size="large" shape="circle">管理活动</i-button>
          <i-button @click="deleteActivity(item)" type="primary" inline size="large" shape="circle">删除活动</i-button>
      </view>
      <div v-else style="display:flex;justify-content:center;">
          <i-button type="primary" inline size="large" shape="circle" style="padding:5px" disabled>管理活动</i-button>
          <i-button type="primary" inline size="large" shape="circle" style="padding:5px" disabled>删除活动</i-button>
      </div>
    </view>
  </div>
</template>

<script>

export default {
  data () {
    return {
      item: {},
      openid: 12
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
      'id': '123', // 活动id标识
      'leader': 123, // 活动发起人
      'members': [
        {'id': 123, 'avatar': 'https://avatars3.githubusercontent.com/u/43805318?s=460&v=4'},
        {'id': 125, 'avatar': 'https://avatars3.githubusercontent.com/u/43805318?s=460&v=4'}
      ]
    }
    this.opend = 123
  },
  methods: {
    'manageActivity': function (item) {
      wx.navigateTo({ url: '/pages/manage/main?id=' + item.id })
    },
    'deleteActivity': function (item) {
      wx.navigateBack({
        delta: 1 // 返回的页面数，如果 delta 大于现有页面数，则返回到首页,
      })
    }
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
