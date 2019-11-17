<template>
  <div>
    <i-tabs current="current">
      <i-tab key=0 title="正在申请" @click='switchTab(0)'></i-tab>
      <i-tab key=1 title="正在进行" @click='switchTab(1)'></i-tab>
      <i-tab key=2 title="已结束" @click='switchTab(2)'></i-tab>
    </i-tabs>
    <i-panel v-if="current===0">
      <view style="padding:15px;">
        <div v-for="(item,index) in applyingItems" :key=index style="padding-bottom:15px">
          <i-card full @click='bindClick(item)' :title="item.title" :extra="item.leaderName" :thumb="item.thumb" i-class="card-thumb">
            <view slot="content">{{item.description}}</view>
            <view slot="footer">{{item.time+" "+item.location}}</view>
          </i-card>
        </div>
      </view>
    </i-panel>
    <i-panel v-if="current===1">
      <view style="padding:15px;">
        <div v-for="(item,index) in applyedItems" :key=index style="padding-bottom:15px">
          <i-card full @click='bindClick(item)' :title="item.title" :extra="item.leaderName" :thumb="item.thumb" i-class="card-thumb">
            <view slot="content">{{item.description}}</view>
            <view slot="footer">{{item.time+" "+item.location}}</view>
          </i-card>
        </div>
      </view>
    </i-panel>
    <i-panel v-if="current===2">
      <view style="padding:15px;">
        <div v-for="(item,index) in endedItems" :key=index style="padding-bottom:15px">
          <i-card full @click='bindClick(item)' :title="item.title" :extra="item.leaderName" :thumb="item.thumb" i-class="card-thumb">
            <view slot="content">{{item.description}}</view>
            <view slot="footer">{{item.time+" "+item.location}}</view>
          </i-card>
        </div>
      </view>
    </i-panel>
  </div>
</template>

<script>

export default {
  data(){
    return {
      current:0
    }
  },
  computed: {
    'applyedItems': function () {
      return this.$store.state.items.filter((item) => {
        let date=new Date(item.time)
        let now=new Date()
        return item.type === 'applyed' && now.getTime()< date.getTime()+86400000
      })
    },
    'applyingItems': function () {
      return this.$store.state.items.filter((item) => {
        return item.type === 'applying'
      })
    },
    'endedItems':function(){
      return this.$store.state.items.filter((item) => {
        let date=new Date(item.time)
        let now=new Date()
        return item.type === 'applyed' && now.getTime()>= date.getTime()+86400000
      })
    }
  },
  components: {},

  methods: {
    'bindClick': function (item) {
      wx.navigateTo({ url: '/pages/activity/main?id=' + item.id })
    },
    'switchTab':function(key){
      this.current=key
    }
  },
  onLoad (options) {
    wx.login({
      success: res => {
        console.log(res)
        this.$store.commit('getUser', 123) //参数为code
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
