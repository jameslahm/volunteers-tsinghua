<template>
  <div>
    <i-message id="message" />
    <i-card title="您的意见">
      <view slot="content">
        <i-input :value="content" type="textarea" @change="changeInput"></i-input>
      </view>
      <view slot="footer">
        <i-button @click="bindClick()" size="small" type="primary">提交</i-button>
      </view>
    </i-card>
  </div>
</template>

<script>
const { $Message } = require('../../../static/iview/base/index');

export default {
  data() {
    return {
      'content':''
    }
  },
  methods: {
    'bindClick': function() {
      this.$store.commit('suggestion',this.content);
      $Message({
        content:'提交成功',
        type:'success'
      })
    },
    'changeInput':function(event){
      this.content=event.target.detail.value
    }
  },
  onLoad () {
  }
};
</script>

<style>
</style>