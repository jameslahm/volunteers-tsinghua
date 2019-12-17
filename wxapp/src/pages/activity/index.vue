<template>
  <div>
    <i-message id="message" />
    <view style="padding:15px;">
      <i-card full :title="item.title" :thumb="item.thumb" i-class="card-thumb">
        <view slot="content">
            活动编号：<br/>{{item.AID}}<br/><br/>
            活动内容：<br/>{{item.content}}
        </view>
        <!-- <view slot="footer">
          <i-panel title="团队成员" hide-border hide-top>
            <i-avatar v-for="(member,index) in item.members" :key=index :src="member.avatar" size=large style="padding:8px;">
            </i-avatar>
          </i-panel>
        </view> -->
      </i-card>
      <i-button v-if="isApplyed" @click='bindClick()' disabled type='primary' size='small'>报名活动</i-button> 
      <i-button v-else @click='bindClick()' type='primary' size='small'>报名活动</i-button> 
    </view>
   </div>
</template>

<script>
const { $Message } = require('../../../static/iview/base/index');

export default {
  data () {
    return {
      itemId: 123
    }
  },
  computed: {
    'item': function () {
      return this.$store.getters.getGlobalItemById(this.itemId) || this.$store.getters.getItemById(this.itemId)
    },
    'isApplyed':function(){
      if(this.$store.state.user.id!=undefined){
        let item=this.$store.getters.getItemById(this.itemId)
        if(item && item.type!='refused')
          return true
        else
          return false
      }
      else{
        return true
      }
    }
  },
  components: {},
  onLoad (options) {
    this.itemId = parseInt(options.id)
    this.$store.commit('getItems')
  },
  methods: {
    'bindClick':function(){
      if(this.$store.state.user.id===undefined){
        $Message({
          content:"抱歉，请先登录",
          type : "warning"
        })
        return
      }
      if(this.isApplyed){
        $Message({
          content:"抱歉，你已经报名了",
          type:'warning'
        })
        return
      }
      if(this.item.appliedRecruits===this.item.totalRecruits){
        $Message({
          content:"抱歉，该活动人数已招满",
          type:'warning'
        })
        return 
      }
      wx.navigateTo({ url: '/pages/apply/main?id=' + this.item.id })
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
  width:30px;
  height:30px;
}
</style>
