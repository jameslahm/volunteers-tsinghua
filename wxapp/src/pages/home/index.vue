<template>
  <div>
    <view>
      <i-sticky>
        <i-sticky-item scrollTop="scrollTop">
          <view
            slot="title"
            style="display: flex;flex-direction: row;justify-content:space-between;"
          >
            <view>活动信息</view>
            <i-icon @click="search()" type="search" size="28" color="#80848f" />
          </view>
        </i-sticky-item>
      </i-sticky>
    </view>
    <i-panel>
      <view style="padding:15px;">
        <div v-for="(item,index) in items" :key="index" style="padding-bottom:15px">
          <i-card
            full
            @click="bindClick(item)"
            :title="item.teamName"
            :extra="item.appliedRecruits+'/'+item.totalRecruits"
            i-class="card-thumb"
          >
            <view slot="content">{{item.title}}</view>
            <view slot="footer">{{item.starttime+" "+item.location}}</view>
          </i-card>
        </div>
      </view>
      <i-page :current="current" :total="total" @change="handleChange">
        <view slot="prev">
          <i-icon type="return"></i-icon>
          Prev
        </view>
        <view slot="next">
          Next
          <i-icon type="enter"></i-icon>
        </view>
      </i-page>
    </i-panel>
  </div>
</template>

<script>
import config from '../../config'

export default {
  data() {
    return {
      scrollTop: 0,
      current:1
    };
  },
  computed: {
    items: function() {
      return this.$store.state.globalItems
    },
    total:function(){
      return this.$store.state.total
    }
  },
  components: {},

  methods: {
    bindClick: function(item) {
      wx.navigateTo({ url: "/pages/activity/main?id=" + item.id });
    },
    search: function() {
      wx.navigateTo({ url: "/pages/search/main" });
    },
    handleChange({target}){
      const type = target.type;
        if (type === 'next') {
            this.current+=1
            this.$store.commit('getGlobalItems',{'page':this.current})
        } else if (type === 'prev') {
            this.current-=1
            this.$store.commit('getGlobalItems',{'page':this.current})
        }
    },
  },
  onLoad(options) {
    // wx.setStorageSync('id','1')
    // wx.setStorageSync('password':'')
    // 查看是否有登录学号
  },
  onShow(){
    if(config.DEBUG){
      wx.setStorageSync('id',1)
      wx.setStorageSync('token','eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3NjUwNjkzNCwiZXhwIjoxNTc5MTg1MzM0fQ.MQ.b3807YrI-VuR1TiJZQAzjsDjNtUdG6uF1l5w99uHiUlyh5--tcyRh_LN7MqdzDCi2VfqnJ0X_QVjQyFAwS2gTA')
    }
    this.$store.commit("getGlobalItems")
    try{
      var id=wx.getStorageSync('id')
      var token=wx.getStorageSync('token')
      // var password=wx.getStorageSync('password')
      if(id){
        this.$store.commit("getUser",id)
        this.$store.state.token=token
        this.$store.commit('verifyToken')
      }
    }catch(e){
      console.log("no login")
    }
  },
  created() {
  },
  onPageScroll(event) {
    this.scrollTop = event.scrollTop;
  }
};
</script>

<style>
.card-thumb image {
  border-radius: 50%;
  width:30px;
  height:30px;
}
</style>
