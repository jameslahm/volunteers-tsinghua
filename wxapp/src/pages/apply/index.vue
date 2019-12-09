<template>
  <div>
    <i-message id="message"/>
    <i-card :thumb="item.thumb" :title="item.title">
      <view slot="content">
        <i-input title="姓名" id="userName" :value="info.userName" type="text" placeholder="name" @change="changeInput"></i-input>
        <i-input title="院系" id="department" :value="info.department" type="text" placeholder="department" @change="changeInput"></i-input>
        <i-input title="微信号" id="wx" :value="info.wx" type="text" placeholder="wx" @change="changeInput"></i-input>
        <i-input title="邮箱" id="email" :value="info.email" type="text" placeholder="email" @change="changeInput"></i-input>
        <i-input title="联系电话" id="phone" :value="info.phone" type="number" placeholder="phone" @change="changeInput"></i-input>
      </view>
      <view slot="footer">
        <i-panel title="报名原因" hide-border hide-top>
          <i-input :value="content" id="content" type="textarea" @change="changeInput"></i-input>
          <i-button @click="bindClick()" size="small" type="primary">提交</i-button>
        </i-panel>
      </view>
    </i-card>
  </div>
</template>

<script>
const { $Message } = require('../../../static/iview/base/index');

export default {
  data() {
    return {
      itemId:0,
      info:{},
      content:''
    }
  },
  computed:{
    'item':function(){
      return this.$store.getters.getGlobalItemById(this.itemId) || this.$store.getters.getItemById(this.itemId)
    },
    'user':function(){
      return this.$store.state.user
    }
  },
  methods: {
    'bindClick': function() {
      this.$store.commit('applyItem',{'content':this.content,'id':this.itemId})
      $Message({
        content:"报名成功",
        type:'success'
      })
      this.$store.commit('getItems')
    },
    'changeInput':function(event){
      if(event.target.id==='content') this.content=event.target.detail.value
      else this.info[event.target.id]=event.target.detail.value
    }
  },
  onLoad (options) {
    this.itemId=options.id
    for (let key in this.$store.state.user) {
      this.info[key] = this.$store.state.user[key];
    }
  }
};
</script>

<style>
</style>