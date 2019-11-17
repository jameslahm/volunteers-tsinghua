<template>
	<div v-if="isLogIn">
		<i-cell @click='bindClick1(user)' :title="user.userName" :label="user.wx" is-link style="padding-top:15px;padding-bottom:15px;">
			<image :src="user.avatar" slot="icon" style="width:28px;height:28px"  mode="aspectFill"></image>
		</i-cell>
		<i-cell-group>
			<i-cell @click='bindClick3()' title="我的活动" is-link></i-cell>
			<i-cell title="我的工时" is-link></i-cell>
			<i-cell title="我的证书" is-link></i-cell>
			<i-cell title="我的关注" is-link></i-cell>
			<i-cell title="意见反馈" is-link></i-cell>
			<i-cell title="投诉中心" is-link></i-cell>
			<i-cell @click='logOut()' title="退出登录" is-link></i-cell>
		</i-cell-group>
	</div>
	<div v-else>
		<view style="justify-content:center;align-items:center;">
			<i-input v-model="schoolId" title="学号" autofocus placeholder="schoolId" ></i-input>
			<i-input v-model="password" title="密码" type="password" placeholder="password"></i-input>
			<i-button @click='bindClick2()' size="default" type="primary">登录</i-button>
		</view>
	</div>
</template>

<script>

export default {
	data(){
		return {
			isLogIn:false,
			schoolId:'',
			password:'',
		}
	},
	computed:{
		user:function(){
			return this.$store.state.user
		}
	},
	onLoad(){
		if(!this.$store.state.user.id){
			this.isLogIn=false
		}
		else{
			this.isLogIn=true
		}
	},
	methods:{
		'bindClick2':function(){
			this.$store.commit('logIn',{'schoolId':this.schoolId,'password':this.password})
		},
		'bindClick1':function(){
			console.log('info')
			wx.navigateTo({url:'/pages/info/main'})
		},
		'logOut':function(){
			this.isLogIn=false
		},
		'bindClick3':function(){
			console.log('my activities')
			wx.navigateTo({url:'/pages/myactivity/main'})
		}
	}
}
</script>

<style>

</style>