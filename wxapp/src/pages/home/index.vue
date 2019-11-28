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
            :title="item.title"
            :extra="item.leaderName"
            :thumb="item.thumb"
            i-class="card-thumb"
          >
            <view slot="content">{{item.description}}</view>
            <view slot="footer">{{item.time+" "+item.location}}</view>
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
      return this.$store.getters.getGlobalItemsByPage(this.current);
    },
    total:function(){
      total=parseInt(this.$store.state.globalItems.length/20)
      if(this.$store.state.globalItems.length%20==0){
        return total
      }
      else{
        return total+1
      }
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
        } else if (type === 'prev') {
            this.current-=1
        }
    },
  },
  onLoad(options) {
    wx.login({
      success: res => {
        console.log(res);
        this.$store.commit("getUser", 123); //参数为code
        this.$store.commit("getGlobalItems");
      },
      fail: () => {
        console.log("error");
      },
      complete: () => {}
    });
  },
  created() {
    this.$store.commit("getItems");
  },
  onPageScroll(event) {
    this.scrollTop = event.scrollTop;
  }
};
</script>

<style>
.card-thumb image {
  border-radius: 50%;
}
</style>
