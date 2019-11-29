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
            :title="item.team"
            :extra="item.applyedRecruits+'/'+item.totalRecruits"
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
    wx.setStorageSync({'key':'schoolId','data':'123'})
    // 查看是否有登录学号
    try{
      var schoolId=wx.getStorageSync('schoolId')
      console.log(schoolId)
      if(schoolId){
        this.$store.commit("getUser",schoolId)
      }
    }catch(e){
      console.log("no login")
    }
  },
  onShow(){
    let params={'page':this.current}
    this.$store.commit("getGlobalItems",params)
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
