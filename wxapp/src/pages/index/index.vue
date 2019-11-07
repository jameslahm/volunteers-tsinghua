<template>
  <div>
    <i-panel title="申请创建">
      <view style="padding:15px;">
        <i-card @click='bindClick(item)' v-for="(item,index) in createdItems" :key=index :title="item.title" :extra="item.leaderName" :thumb="item.thumb" i-class="card-thumb">
          <view slot="content">{{item.description}}</view>
          <view slot="footer">{{item.time+" "+item.location}}</view>
        </i-card>
      </view>
    </i-panel>
    <i-panel title="申请加入">
      <view style="padding:15px;">
        <i-card @click='bindClick(item)' v-for="(item,index) in applyedItems" :key=index :title="item.title" :extra="item.leaderName" :thumb="item.thumb" i-class="card-thumb">
          <view slot="content">{{item.description}}</view>
          <view slot="footer">{{item.time+" "+item.location}}</view>
        </i-card>
      </view>
    </i-panel>
    <i-panel title="正在申请创建">
      <view style="padding:15px;">
        <i-card @click='bindClick(item)' v-for="(item,index) in creatingItems" :key=index :title="item.title" :extra="item.leaderName" :thumb="item.thumb" i-class="card-thumb">
          <view slot="content">{{item.description}}</view>
          <view slot="footer">{{item.time+" "+item.location}}</view>
        </i-card>
      </view>
    </i-panel>
    <i-panel title="正在申请加入">
      <view style="padding:15px;">
        <i-card @click='bindClick(item)' v-for="(item,index) in applyingItems" :key=index :title="item.title" :extra="item.leaderName" :thumb="item.thumb" i-class="card-thumb">
          <view slot="content">{{item.description}}</view>
          <view slot="footer">{{item.time+" "+item.location}}</view>
        </i-card>
      </view>
    </i-panel>
  </div>
</template>

<script>

export default {
  computed: {
    'applyedItems': function () {
      return this.$store.state.items.filter((item) => {
        return item.type === 'applyed'
      })
    },
    'applyingItems': function () {
      return this.$store.state.items.filter((item) => {
        return item.type === 'applying'
      })
    },
    'createdItems': function () {
      return this.$store.state.items.filter((item) => {
        return item.type === 'created'
      })
    },
    'creatingItems': function () {
      return this.$store.state.items.filter((item) => {
        return item.type === 'creating'
      })
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
        this.$store.commit('setUserId', 123)
      },
      fail: () => { console.log('error') },
      complete: () => {}
    })
  },
  created () {
    this.$store.commit('getItems')
  }
}
</script>

<style>
.card-thumb image {
  border-radius: 50%;
}
</style>
