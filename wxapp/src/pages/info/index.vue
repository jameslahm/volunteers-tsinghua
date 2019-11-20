<template>
  <div>
    <i-message id="message" />
    <i-card :thumb="info.avatar" title="个人信息">
      <view slot="content">
        <i-input title="姓名" id="userName" :value="info.userName" type="text" placeholder="name" @change="changeInput"></i-input>
        <i-input title="院系" id="department" :value="info.department" type="text" placeholder="department" @change="changeInput"></i-input>
        <i-input title="微信号" id="wx" :value="info.wx" type="text" placeholder="wx" @change="changeInput"></i-input>
        <i-input title="邮箱" id="email" :value="info.email" type="text" placeholder="email" @change="changeInput"></i-input>
        <i-input title="联系电话" id="phone" :value="info.phone" type="number" placeholder="phone" @change="changeInput"></i-input>
      </view>
      <view slot="footer">
        <i-panel title="个人简介" hide-border hide-top>
          <i-input :value="info.profile" id="profile" type="textarea" @change="changeInput"></i-input>
          <i-button @click="bindClick()" size="small" type="primary">保存</i-button>
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
      info: {}
    };
  },
  methods: {
    'bindClick': function() {
      this.$store.commit('changeInfo',this.info);
      $Message({
        content:'保存成功',
        type:'success'
      })
    },
    'changeInput':function(event){
      this.info[event.target.id]=event.target.detail.value
    }
  },
  onLoad () {
    for (let key in this.$store.state.user) {
      this.info[key] = this.$store.state.user[key];
    }
  }
};
</script>

<style>
</style>