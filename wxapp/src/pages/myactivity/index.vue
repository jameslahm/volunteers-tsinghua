<template>
  <div>
    <i-tabs current="current" @change="switchTab">
      <i-tab key='0' title="正在申请" :i-class="selected[0]"></i-tab>
      <i-tab key='1' title="正在进行" :i-class="selected[1]"></i-tab>
      <i-tab key='2' title="已结束" :i-class="selected[2]"></i-tab>
    </i-tabs>
    <i-panel v-if="current==='0'">
      <view style="padding:15px;">
        <div v-for="(item,index) in applyingItems" :key=index style="padding-bottom:15px">
          <i-card full @click='bindClick(item)' :title="item.title" :extra="item.appliedRecruits+'/'+item.totalRecruits" i-class="card-thumb">
            <view slot="content">{{item.title}}</view>
            <view slot="footer">{{item.starttime+" "+item.location}}</view>
          </i-card>
        </div>
      </view>
    </i-panel>
    <i-panel v-if="current==='1'">
      <view style="padding:15px;">
        <div v-for="(item,index) in appliedItems" :key=index style="padding-bottom:15px">
          <i-card full @click='bindClick(item)' :title="item.title" :extra="item.appliedRecruits+'/'+item.totalRecruits" i-class="card-thumb">
            <view slot="content">{{item.title}}</view>
            <view slot="footer">{{item.starttime+" "+item.location}}</view>
          </i-card>
        </div>
      </view>
    </i-panel>
    <i-panel v-if="current==='2'">
      <view style="padding:15px;">
        <div v-for="(item,index) in endedItems" :key=index style="padding-bottom:15px">
          <i-card full @click='bindClick(item)' :title="item.title" :extra="item.appliedRecruits+'/'+item.totalRecruits" i-class="card-thumb">
            <view slot="content">{{item.title}}</view>
            <view slot="footer">{{item.starttime+" "+item.location}}</view>
          </i-card>
        </div>
      </view>
    </i-panel>
  </div>
</template>

<script>

export default {
  data(){
    return {
      current:'0',
      selected:[
        'selected',
        '',
        ''
      ]
    }
  },
  computed: {
    'appliedItems': function () {
      return this.$store.state.items.filter((item,index) => {
        let date=new Date(item.time)
        let now=new Date()
        console.log(item)
        return item.type === 'applied' && now.getTime()< (date.getTime()+86400000)
      })
    },
    'applyingItems': function () {
      return this.$store.state.items.filter((item) => {
        return item.type === 'applying'
      })
    },
    'endedItems':function(){
      return this.$store.state.items.filter((item) => {
        let date=new Date(item.time)
        let now=new Date()
        return item.type === 'applied' && now.getTime()>= (date.getTime()+86400000)
      })
    }
  },
  components: {},

  methods: {
    'bindClick': function (item) {
      wx.navigateTo({ url: '/pages/activity/main?id=' + item.id })
    },
    'switchTab':function({target}) {
      this.current=target.key
      for(let i=0;i<this.selected.length;i++){
        this.selected[i]=''
      }
      this.selected[parseInt(this.current)]='selected'
    }
  },
  onShow () {
    this.$store.commit('getItems')
  }
}
</script>

<style>
.card-thumb image {
  border-radius: 50%;
}
.selected{
  color:#2d8cf0;
}
</style>
