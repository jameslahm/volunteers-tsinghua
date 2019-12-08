import Vuex from 'vuex'
import Vue from 'vue'
import { get, post } from '../utils/api'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    items: [], // 用户参加的活动,分页，默认20个
    user: {},
    messages: [], // 用户消息，
    globalItems: [], // 所有活动，分页默认20个
    total: 0, // 所有globalItems总数
    token: '',
    password: ''
  },
  getters: {
    'getItemById': (state) => {
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
    getItems (state, page) {
      get({ 'url': `/users/${state.user.id}/activities`, 'data': {'page': page} }).then((res) => {
        state.items = res
      })
    },
    getMessages (state) {
      get({ 'url': `/users/${state.user.id}/messages` }).then((res) => {
        state.messages = res
        state.messages.forEach(elem => {
          elem.decription = elem.content.slice(0, 20) + '...'
        })
      })
    },
    changeIsRead (state, id) {
      state.messages.forEach(elem => {
        if (elem.id === id) {
          elem.isRead = true
          get({ 'url': `/messages/${elem.id}/changeIsRead` })
        }
      })
    },
    getUser (state, id) {
      console.log(id)
      // post({'url': '/token', 'data': {'schoolId': state.user.schoolId, 'password': state.password}}).then((res) => {
      //   state.token = res.token
      // })
      get({ 'url': `/users/${id}` }).then(res => {
        console.log(res)
        state.user = res
        console.log('User')
      })
    },
    logIn (state, data) {
      post({ 'url': '/auth/login', 'data': { 'schoolId': data.schoolId, 'password': data.password } }).then(res => {
        state.user = res
        wx.setStorageSync({
          key: 'schoolId',
          data: state.user.schoolId
        })
      })
    },
    logOut (state) {
      state.user = undefined
    },
    changeInfo (state, info) {
      for (let k in info) {
        state.user[k] = info[k]
      }
      post({ 'url': `/users/${state.user.id}`, 'data': state.user })
    },
    getGlobalItems (state, params) {
      get({ 'url': '/activities', 'data': params }).then(res => {
        console.log(res)
        state.globalItems = res.items
        state.total = res.total
        console.log(res.total)
      })
    },
    applyItem (state, data) {
      get({'url': `/users/${state.user.id}/apply`, 'data': data}).then(res => {
        console.log(res)
      })
    },
    clearGlobalItems (state) {
      state.globalItems = []
    },
    deleteMessage (state, id) {
      get(`/message/${id}/delete`).then(res => {
        console.log(res)
      })
    }
  }
})

export default store
