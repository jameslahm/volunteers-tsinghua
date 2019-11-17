<template>
  <div>
    <i-message id="message" />
    <view style="padding:15px;">
      <i-card full :title="item.title" :extra="item.extra" :thumb="item.thumb" i-class="card-thumb">
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
      <i-button @click='bindClick()' type='primary' size='small'>报名活动</i-button> 
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
      return this.$store.getters.getGlobalItemById(this.itemId)
    }
  },
  components: {},
  onLoad (options) {
    this.itemId = options.id
    console.log(this.itemId)
  },
  methods: {
    'bindClick':function(){
      if(this.item.applyedRecruits===this.item.totalRecruits){
        $Message({
          content:"抱歉，该活动人数已招满",
          type:'warning'
        })
      }
      else{
        wx.navigateTo({ url: '/pages/apply/main?id=' + this.item.id })
      }
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
