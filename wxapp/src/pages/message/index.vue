<template>
    <i-card :thumb="message.team.avatar" title="通知" i-class="card-thumb">
        <view slot="content">{{message.content}}</view>
        <view slot="footer">
            <p>请扫码入群</p>
            <img :src="message.qrCode">
            <i-button @click="bindClick()" size="small" type="primary">删除消息</i-button>
        </view>
    </i-card>
</template>

<script>
export default {
    data(){
        return {
            messageId:''
        }
    },
    methods:{
        'bindClick':function(){
            this.$store.commit('deleteMessage',messageId)
        }
    },
    computed:{
        message:function(){
            return this.$store.getters.getMessageById(this.messageId)
        }
    },
    onLoad(options){
        this.messageId=options.id
        console.log(this.messageId)
    }
}
</script>

<style>
.card-thumb {
    border-radius: 50%;
}
</style>