<template>
    <i-card :thumb="message.team.avatar" title="通知" i-class="card-thumb">
        <view slot="content">{{message.content}}</view>
        <view slot="footer">
            <p>请扫码入群</p>
            <img :src="message.qrCode">
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