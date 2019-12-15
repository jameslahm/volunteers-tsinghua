<template>
<div>
    <i-message id="message" />
    <i-card :thumb="message.team.avatar" title="通知" i-class="card-thumb">
        <view slot="content">{{message.content}}
            <p>请扫码入群</p>
            <img :src="message.qrcode" mode='widthFix'>
            <i-button @click="bindClick()" size="small" type="primary">删除消息</i-button>
        </view>
    </i-card>
</div>
</template>

<script>

const { $Message } = require('../../../static/iview/base/index');

export default {
    data(){
        return {
            messageId:''
        }
    },
    methods:{
        'bindClick':function(){
            if(this.$store.commit('deleteMessage',this.messageId)){
                $Message({
                    content:'删除成功',
                    type:'success'
                })
            }
            else{
                $Message({
                    content:'抱歉，您的登录凭证已失效，请重新登录',
                    type:'warning'
                })
            }
        }
    },
    computed:{
        message:function(){
            return this.$store.getters.getMessageById(this.messageId)
        }
    },
    onLoad(options){
        this.messageId=options.id
    }
}
</script>

<style>
.card-thumb {
    border-radius: 50%;
}
</style>