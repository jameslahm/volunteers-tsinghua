<template>
  <div>
    <i-message id="message"/>
    <i-panel title="审批消息">
    <i-cell-group>
      <i-cell  @click='bindClick(item)' :title="item.team.teamName" v-for="(item,index) in messages" :label="item.decription" :key=index is-link>
          <i-badge v-if="item.isRead" slot="icon"><image :src="item.team.avatar" style="width:28px;height:28px"  mode="aspectFill"></image></i-badge>
          <i-badge v-else dot slot="icon"><image :src="item.team.avatar" style="width:28px;height:28px"  mode="aspectFill"></image></i-badge>
      </i-cell>
    </i-cell-group>
    </i-panel>
  </div>
</template>

<script>
const { $Message } = require('../../../static/iview/base/index');

export default {
  data(){
    return {
      time:''
    }
  },
  onLoad(){
    let time=new Date()
    let h=time.getHours()
    let m=time.getMinutes()
    this.time=h+":"+m
  },
	computed: {
			userId:function(){
					return this.$store.state.user.id
			},
			messages:function(){
        if(this.$store.state.user.id)
					return this.$store.state.messages
			}
	},
	onShow () {
      if(this.$store.state.user.id){
        this.$store.commit('getMessages')
        this.$store.commit('getItems')
      }
      else{
        $Message({
        content:"抱歉，您还未登录",
        type:'warning'
      })
      }
  },
  methods:{
    'bindClick':function(item){
      if(this.$store.state.token===undefined){
        $Message({
        content:"抱歉，您的登录凭证已失效，请重新登录",
        type:'warning'
        })
        return
      }
      this.$store.commit('changeIsRead',item.id)
      wx.navigateTo({ url: '/pages/message/main?id=' + item.id })
    }
  }
}
</script>