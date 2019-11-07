<template>
	<div>
		<i-input title="时间" v-model="item.time" type=text placeholder="请输出年月日格式 例如:2019年10月1日">
		</i-input>
		<i-input title="地点" v-model="item.location" type=text placeholder="请输出活动地点">
		</i-input>
		<i-panel title="简述">
  		<i-input v-model="item.description" type="textarea" maxlength=50>
  		</i-input>
  	</i-panel>
		<i-panel title="活动内容">
			<i-input v-model="item.content" type="textarea">
			</i-input>
		</i-panel>
		<view v-if="openid===item.leader">
          <i-button @click="manageActivity(item)" type="warning" size="small" shape="circle">管理活动</i-button>
      </view>
	</div>
</template>

<script>

export default {

}
</script>

<style>

</style>