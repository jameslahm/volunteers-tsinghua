<template>
  <div> 
  <i-toast id="toast" />
  <view style="display: flex;flex-direction: row;align-items:center;width:100%;position:relative">
    <i-icon v-if="type.length===0" type="search" size='28'></i-icon>
    <i-icon v-else type="return" size=28 @click="clickReturn" ></i-icon>
    <view style="width:80%">
      <i-input :value="text" :placeholder="placeholder" type='text' @change="changeInput" @confirm="toSearch"></i-input>
    </view>
  </view>
  <i-panel v-if="notInputing">
    <view>
    <i-grid>
      <i-row>
          <i-grid-item>
            <view style="display:flex;flex-direction:column;justify-content:center;align-items:center" @click="bindClick1('activity')">
              <i-icon size="25" type="activity" />
              <i-grid-label>活动名称</i-grid-label>
            </view>
          </i-grid-item>
          <i-grid-item>
            <view style="display:flex;flex-direction:column;justify-content:center;align-items:center" @click="bindClick1('coordinates')">
              <i-icon size="25" type="coordinates" />
              <i-grid-label>活动地点</i-grid-label>
            </view>
          </i-grid-item>
          <i-grid-item>
            <view style="display:flex;flex-direction:column;justify-content:center;align-items:center" @click="bindClick1('time')">
              <i-icon size="25" type="time" />
              <i-grid-label>活动时间</i-grid-label>
            </view>
          </i-grid-item>
      </i-row>
      <i-row>
          <i-grid-item>
            <view style="display:flex;flex-direction:column;justify-content:center;align-items:center" @click="bindClick1('group')">
              <i-icon size="25" type="group" />
              <i-grid-label>举办方</i-grid-label>
            </view>
          </i-grid-item>
          <i-grid-item>
            <view style="display:flex;flex-direction:column;justify-content:center;align-items:center" @click="bindClick1('barrage')">
              <i-icon size="25" type="barrage" />
              <i-grid-label>活动编号</i-grid-label>
            </view>
          </i-grid-item>
      </i-row>
    </i-grid>
    </view>
  </i-panel>
  <i-panel v-else>
      <view style="padding:15px;">
        <div v-for="(item,index) in items" :key=index style="padding-bottom:15px">
          <i-card
            full
            @click="bindClick2(item)"
            :title="item.teamName"
            :extra="item.appliedRecruits+'/'+item.totalRecruits"
            i-class="card-thumb"
          >
            <view slot="content">{{item.title}}</view>
            <view slot="footer">{{item.starttime+" "+item.location}}</view>
          </i-card>
        </div>
      </view>
    </i-panel>
  </div>
</template>

<script>
const { $Toast } = require('../../../static/iview/base/index');

export default {
  data() {
    return {
      notInputing:true,
      text:'',
      placeholder:'搜索',
      dict:{
        'activity':"按活动名称搜索",
        'coordinates':"按活动地点搜索",
        'time':"按活动时间搜索",
        'group':"按活动举办方搜索",
        'barrage':"按活动编号搜索"
      },
      type:''
    }
  },
  computed:{
    'items':function(){
      return this.$store.state.globalItems
    }
  },
  onShow(){
    this.text=''
    this.type='general'
  },
  methods: {
    'changeInput':function(e){
      this.text=e.target.detail.value
      let params={'text':this.text,'type':this.type}
      if(this.text.length!=0){
        this.$store.commit('getGlobalItems',params)
        this.notInputing=false
      }
      else{
        if(this.type==='general'){
          this.notInputing=true
        }
      }
    },
    'toSearch':function(e){
      this.text=e.target.detail.value
      let params={'text':this.text,'type':this.type}
      if(this.text.length!=0){
        this.$store.commit('getGlobalItems',params)
        this.notInputing=false
      }
      else{
        $Toast({
          content:"Please input some text",
          type:'warning'
        })
        this.notInputing=true
      }
    },
    'bindClick1':function(key){
      this.type=key
      this.placeholder=this.dict[key]
      this.notInputing=false
      this.$store.commit('clearGlobalItems')
    },
    'bindClick2':function(item){
      wx.navigateTo({ url: '/pages/activity/main?id=' + item.id })
    },
    'clickReturn':function(){
      this.notInputing=true
      this.type='general'
      this.text=''
      this.placeholder="搜索"
    }
  },
  onLoad (options) {
  }
};
</script>

<style>
</style>