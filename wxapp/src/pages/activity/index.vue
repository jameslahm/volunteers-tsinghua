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
      <view v-if="openid===item.leader">
          <i-button @click="manageActivity(item)" type="primary" size="small" shape="circle">管理活动</i-button>
      </view>
      <!-- <div v-else style="display:flex;justify-content:center;">
          <i-button type="primary" inline size="large" shape="circle" style="padding:5px" disabled>管理活动</i-button>
          <i-button type="primary" inline size="large" shape="circle" style="padding:5px" disabled>删除活动</i-button>
      </div> -->
    </view>
  </div>
</template>

<script>

export default {
  data () {
    return {
      itemId: 123
    }
  },
  computed: {
    userId: function () {
      return this.$store.state.userId
    },
    item: function () {
      return this.$store.getters.getItemById(this.itemId)
    }
  },
  components: {},
  onLoad (options) {
    this.itemId = options.id
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
