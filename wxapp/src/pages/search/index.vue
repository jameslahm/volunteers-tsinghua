<template>
  <div> 
  <view style="display: flex;flex-direction: row;align-items:center">
    <i-icon type="search" size='28'></i-icon>
    <i-input type='text' placeholder="搜索" @input='changeInput' @confirm="toSearch"/>
  </view>
  <i-panel>
    <view>
    <i-grid>
      <i-row>
          <i-grid-item>
            <view>
              <i-icon size="25" type="activity" />
              <i-grid-label>活动名称</i-grid-label>
            </view>
          </i-grid-item>
          <i-grid-item>
            <i-grid-icon>
                <i-icon size="25" type="coordinates" />
                <i-grid-label>地点</i-grid-label>
            </i-grid-icon>
          </i-grid-item>
          <i-grid-item>
              <i-grid-icon>
                  <i-icon size="25" type="time" />
                  <i-grid-label>时间</i-grid-label>
              </i-grid-icon>
          </i-grid-item>
      </i-row>
      <i-row>
          <i-grid-item>
              <i-grid-icon>
                  <i-icon size="25" type="group" />
                  <i-grid-label>举办方</i-grid-label>
              </i-grid-icon>
          </i-grid-item>
          <i-grid-item>
              <i-grid-icon>
                  <i-icon size="25" type="barrage" />
                  <i-grid-label>活动编号</i-grid-label>
              </i-grid-icon>
          </i-grid-item>
      </i-row>
    </i-grid>
    </view>
  </i-panel>

  </div>
</template>

<script>
const { $Message } = require('../../../static/iview/base/index');

export default {
  data() {
  },
  computed:{
  },
  methods: {
  },
  onLoad (options) {
  }
};
</script>

<style>
</style>