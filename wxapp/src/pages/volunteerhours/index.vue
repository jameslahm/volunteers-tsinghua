<template>
<div>
  <i-panel title="志愿工时">
    <view style="padding: 15px;font-size:50px">{{hours}}<span style="font-size:10px">hours</span></view>
  </i-panel>
  <i-panel>
      <view style="padding:15px;">
        <div v-for="(item,index) in items" :key="index" style="padding-bottom:15px">
          <i-card
            full
            @click="bindClick(item)"
            :title="item.teamName"
            :extra="item.hours+'h'"
            i-class="card-thumb"
          >
            <view slot="content">{{item.title}}</view>
            <view slot="footer">{{item.starttime+" "+item.location}}</view>
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
    }
  },
  computed:{
    'hours':function(){
      let hours=0
      this.$store.state.items.filter(elem=>{
        return elem.type==='finished'
      }).forEach(elem => {
        console.log(elem)
        hours+=elem.hours
      })
      return hours
    },
    'items':function(){
      return this.$store.state.items.filter(elem=>{
        return elem.type==='finished'
      })
    }
  },
  methods:{
    'bindClick':function(item){
      wx.navigateTo({ url: "/pages/activity/main?id=" + item.id });
    }
  }
};
</script>

<style>
</style>