<template>
  <div>
    <i-cell-group>
        <i-cell  @click='bindClick(item)' :title="item.team.name" v-for="(item,index) in messages" :label="item.decription" :key=index is-link>
            <i-badge v-if="item.isRead" slot="icon"><image :src="item.team.avatar" style="width:28px;height:28px"  mode="aspectFill"></image></i-badge>
            <i-badge v-else dot slot="icon"><image :src="item.team.avatar" style="width:28px;height:28px"  mode="aspectFill"></image></i-badge>
        </i-cell>
    </i-cell-group>
  </div>
</template>

<script>
export default {
	computed: {
			userId:function(){
					return this.$store.state.user.id
			},
			messages:function(){
					return this.$store.state.messages
			}
	},
	onShow () {
      this.$store.commit('getMessages')
      console.log("notice")
  },
  methods:{
    'bindClick':function(item){
      this.$store.commit('changeIsRead',item.id)
      wx.navigateTo({ url: '/pages/message/main?id=' + item.id })
    }
  }
}
</script>