<template>
	<div v-if="isLogIn">
		<i-message id="message"/>
		<i-cell @click='bindClick1(user)' :title="user.userName" :label="user.wx" is-link style="padding-top:15px;padding-bottom:15px;">
			<image :src="user.avatar" slot="icon" style="width:28px;height:28px"  mode="aspectFill"></image>
		</i-cell>
		<i-cell-group>
			<i-cell @click='bindClick6()' title='签到'></i-cell>
			<i-cell @click='bindClick3()' title="我的活动" is-link></i-cell>
			<i-cell @click='bindClick4()' title="我的工时" is-link></i-cell>
			<i-cell title="我的证书" is-link></i-cell>
			<i-cell title="我的关注" is-link></i-cell>
			<i-cell @click='bindClick5()' title="意见反馈" is-link></i-cell>
			<i-cell @click='logOut()' title="退出登录" is-link></i-cell>
		</i-cell-group>
	</div>
	<div v-else>
		<view style="justify-content:center;align-items:center;">
			<i-input v-model="schoolId" title="学号" autofocus placeholder="schoolId" ></i-input>
			<i-input v-model="password" title="密码" type="password" placeholder="password"></i-input>
			<i-button @click='bindClick2()' size="default" type="primary">登录</i-button>
		</view>
		<small style="font-size:10px">&emsp;Tips:&emsp;您可以直接点击登录按钮进入清华学号认证</small>
	</div>
</template>

<script>
import { get, post } from '../../utils/api'
const { $Message } = require('../../../static/iview/base/index');

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
	onShow(){
		if(!this.$store.state.user.id){
			this.isLogIn=false
		}
		else{
			this.isLogIn=true
			this.$store.commit('getItems')
		}
	},
	onLoad(){
	},
	methods:{
		'bindClick2':function(){
			wx.navigateToMiniProgram({  
				"appId": "wx1ebe3b2266f4afe0",  
				"path": "pages/index/index",  
				"envVersion": "trial",  
				"extraData": {   
					"origin": "miniapp",   
					"type": "id.tsinghua"  
					},
				fail(res){
					console.log(res)
				},
			})
		},
		'bindClick1':function(){
			wx.navigateTo({url:'/pages/info/main'})
		},
		'logOut':function(){
			this.isLogIn=false
			this.$store.commit('logOut')
		},
		'bindClick3':function(){
			wx.navigateTo({url:'/pages/myactivity/main'})
		},
		'bindClick4':function(){
			wx.navigateTo({url:'/pages/volunteerhours/main'})
		},
		'bindClick5':function(){
			wx.navigateTo({url:'/pages/suggestion/main'})
		},
		'bindClick6':function(){
			wx.scanCode({
      			success: (res) => {
						var data = parseInt(res.result);
						post({url:`/activities/${data}/signin`,data:{'token':this.$store.state.token}}).then(res=>{
							console.log(res)
							$Message({
								content:'签到成功',
								type:'success'
							})
						})
				  }
			})	
		}
	}
}
</script>

<style>
</style>