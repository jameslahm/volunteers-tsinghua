import Vuex from 'vuex'
import Vue from 'vue'
import { get, post } from '../utils/api'
import config from '../config'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    items: [], // 用户参加的活动,分页，默认20个
    user: {},
    messages: [], // 用户消息，
    globalItems: [], // 所有活动，分页默认20个
    total: 0, // 所有globalItems总数
    token: ''
  },
  getters: {
    'getItemById': (state) => {
      console.log(state.items)
      return function (id) {
        return state.items.filter((item) => {
          return item.id === parseInt(id)
        })[0]
      }
    },
    'getMessageById': (state) => {
      return function (id) {
        return state.messages.filter((item) => {
          return item.id === parseInt(id)
        })[0]
      }
    },
    'getGlobalItemById': (state) => {
      return function (id) {
        return state.globalItems.filter((item) => {
          return item.id === parseInt(id)
        })[0]
      }
    }
  },
  mutations: {
    getItems (state) {
      console.log('getItems')
      get({ 'url': `/users/${state.user.id}/activities` }).then((res) => {
        state.items = res
        state.items.forEach(elem => {
          elem.thumb = config.host + ':' + config.port + elem.thumb
        })
        console.log(state.items)
      })
    },
    getMessages (state) {
      get({ 'url': `/users/${state.user.id}/messages` }).then((res) => {
        state.messages = res
        state.messages.forEach(elem => {
          elem.decription = elem.content.slice(0, 20) + '...'
          elem.qrcode = config.host + ':' + config.port + elem.qrcode
        })
      })
    },
    changeIsRead (state, id) {
      state.messages.forEach(elem => {
        if (elem.id === id) {
          elem.isRead = true
          post({ 'url': `/messages/${elem.id}/changeIsRead`, 'data': {'token': state.token} })
        }
      })
    },
    getUser (state, id) {
      get({ 'url': `/users/${id}` }).then(res => {
        state.user = res
        console.log(state.user)
      })
    },
    logOut (state) {
      state.user = {}
      state.token = ''
    },
    changeInfo (state, info) {
      for (let k in info) {
        state.user[k] = info[k]
      }
      var data = info
      data.token = state.token
      post({ 'url': `/users/${state.user.id}`, 'data': data })
    },
    getGlobalItems (state, params) {
      get({ 'url': '/activities', 'data': params }).then(res => {
        console.log(res)
        state.globalItems = res.items
        state.globalItems.forEach(elem => {
          elem.thumb = config.host + ':' + config.port + elem.thumb
        })
        state.total = res.total
        console.log(state.globalItems)
      })
    },
    applyItem (state, data) {
      data.token = state.token
      post({'url': `/users/${state.user.id}/apply`, 'data': data}).then(res => {
      })
    },
    clearGlobalItems (state) {
      state.globalItems = []
    },
    deleteMessage (state, id) {
      post({'url': `/messages/${id}/delete`, 'data': {'token': state.token}}).then(res => {
      })
    },
    verifyTHU (state, token) {
      post({'url': '/verifyTHU', 'data': {'token': token}}).then((res) => {
        state.user = res.user
        state.token = res.token
        wx.setStorageSync('id', state.user.id)
        wx.setStorageSync('token', state.token)
        wx.getSetting({
          success (res) {
            if (res.authSetting['scope.userInfo']) {
              // 已经授权，可以直接调用 getUserInfo 获取头像昵称
              wx.getUserInfo({
                success: function (res) {
                  state.user.avatar = res.userInfo.avatarUrl
                  var data = state.user
                  console.log(state.user)
                  data.token = state.token
                  post({ 'url': `/users/${state.user.id}`, 'data': data })
                }
              })
            } else {
              wx.authorize({
                scope: 'scope.userInfo',
                success () {
                  wx.getUserInfo({
                    success: function (res) {
                      state.user.avatar = res.userInfo.avatarUrl
                      var data = state.user
                      console.log(state.user)
                      data.token = state.token
                      post({ 'url': `/users/${state.user.id}`, 'data': data })
                    }
                  })
                }
              })
            }
          }
        })
        console.log('Avatar')
      })
    },
    suggestion (state, content) {
      post({'url': '/suggestions', 'data': {'content': content}}).then(res => {
        console.log(res)
      })
    }
  }
})

export default store
