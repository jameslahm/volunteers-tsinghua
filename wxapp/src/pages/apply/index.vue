<template>
  <div>
    <i-message id="message"/>
    <i-card :thumb="item.thumb" title="item.title">
      <view slot="content">
        <i-input title="姓名" v-model="info.userName" type="text" placeholder="name"></i-input>
        <i-input title="院系" v-model="info.department" type="text" placeholder="department"></i-input>
        <i-input title="微信号" v-model="info.wx" type="text" placeholder="wx"></i-input>
        <i-input title="邮箱" v-model="info.email" type="text" placeholder="email"></i-input>
        <i-input title="联系电话" v-model="info.phone" type="number" placeholder="phone"></i-input>
      </view>
      <view slot="footer">
        <i-panel title="报名原因" hide-border hide-top>
          <i-input v-model="content" type="textarea"></i-input>
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
      return this.$store.getters.getGlobalItemById(this.itemId)
    },
    'user':function(){
      return this.$store.state.user
    }
  },
  methods: {
    bindClick: function() {
      this.$store.commit('applyItem',{'content':this.content})
      $Message({
        content:"报名成功",
        type:'success'
      })
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