<template>
  <div>
    <i-card :thumb="info.avatar" title="个人信息">
      <view slot="content">
        <i-input title="姓名" v-model="info.userName" type="text" placeholder="name"></i-input>
        <i-input title="院系" v-model="info.department" type="text" placeholder="department"></i-input>
        <i-input title="微信号" v-model="info.wx" type="text" placeholder="wx"></i-input>
        <i-input title="邮箱" v-model="info.email" type="text" placeholder="email"></i-input>
        <i-input title="联系电话" v-model="info.phone" type="number" placeholder="phone"></i-input>
      </view>
      <view slot="footer">
        <i-panel title="个人简介" hide-border hide-top>
          <i-input v-model="info.profile" type="textarea"></i-input>
          <i-button @click="bindClick()" size="small" type="primary">保存</i-button>
        </i-panel>
      </view>
    </i-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      info: {}
    };
  },
  methods: {
    bindClick: function() {
      this.$store.commit('changeInfo',this.info);
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