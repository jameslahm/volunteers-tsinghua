import Vuex from 'vuex'
import Vue from 'vue'
import {get} from '../utils/api'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    items: [],
    userId: 123
  },
  getters: {
    'getItemById': (state) => {
      return function (id) {
        return state.items.filter((item) => {
          return item.id === id
        })[0]
      }
    }
  },
  mutations: {
    getItems (state) {
      get({'url': '/users/123/activities'}).then((res) => {
        state.items = res
      })
    },
    setUserId (state, value) {
      state.userId = value
    }
  }
})

export default store
