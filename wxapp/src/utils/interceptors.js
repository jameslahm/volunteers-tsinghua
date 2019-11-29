import config from '@/config'
import Mock from 'mockjs'

var Fly = require('flyio/dist/npm/wx')

var fly = new Fly()
let DEBUG = config.DEBUG
let host = config.host

fly.config.timeout = 1000
fly.config.baseUrl = config.host

fly.interceptors.request.use((request) => {
  request.headers['X-Tag'] = 'flyio'
  if (DEBUG) {
    if (request.url === `${host}/users/123/activities`) {
      let res = []
      for (let i = 0; i < 20; i++) {
        res.push(Mock.mock({
          'id': Mock.Random.id(),
          'AID': Mock.Random.guid().slice(0, 12),
          'title': Mock.Random.csentence(8),
          'thumb': Mock.Random.image('28x28'),
          'team': Mock.Random.csentence(8),
          'content': Mock.Random.cparagraph(5),
          'starttime': Mock.Random.datetime(),
          'endtime': Mock.Random.datetime(),
          'location': Mock.Random.county(),
          'type|1': ['applying', 'applyed'],
          'totalRecruits': Mock.Random.integer(1, 20),
          'applyedRecruits': Mock.Random.integer(1, 20),
          'members': [
            { 'userid': Mock.Random.id(), 'avatar': Mock.Random.image() },
            { 'userid': Mock.Random.id(), 'avatar': Mock.Random.image() }
          ]
        }))
      }
      return Promise.resolve(res)
    }
    if (request.url === `${host}/users/123/messages`) {
      let res = []
      for (let i = 0; i < 5; i++) {
        res.push(Mock.mock({
          'id': Mock.Random.id(),
          'qrCode': Mock.Random.image('28x28'),
          'content': Mock.Random.cparagraph(5),
          'time': Mock.Random.datetime(),
          'team': {
            'id': Mock.Random.id(),
            'avatar': Mock.Random.image(),
            'name': Mock.Random.cname()
          },
          'isRead': Mock.Random.boolean()
        }))
      }
      return res
    }
    if (request.url === `${host}/users/123`) {
      let res = {}
      res.id = Mock.Random.id()
      res.openId = Mock.Random.guid()
      res.userName = Mock.Random.cname()
      res.wx = Mock.Random.id()
      res.email = Mock.Random.email()
      res.avatar = Mock.Random.image('28x28')
      res.department = Mock.Random.name()
      res.phone = Mock.Random.string('number')
      res.profile = Mock.Random.cparagraph()
      res.schoolId = Mock.Random.id()
      return res
    }
    if (request.url === `${host}/activities`) {
      let res = {'items': [], 'total': 100}
      for (let i = 0; i < 20; i++) {
        res.items.push(Mock.mock({
          'id': Mock.Random.id(),
          'AID': Mock.Random.guid().slice(0, 12),
          'title': Mock.Random.csentence(8),
          'thumb': Mock.Random.image('28x28'),
          'team': Mock.Random.csentence(8),
          'content': Mock.Random.cparagraph(5),
          'starttime': Mock.Random.datetime(),
          'endtime': Mock.Random.datetime(),
          'location': Mock.Random.county(),
          'type|1': ['applying', 'applyed'],
          'totalRecruits': Mock.Random.integer(1, 20),
          'applyedRecruits': Mock.Random.integer(1, 20),
          'members': [
            { 'userid': Mock.Random.id(), 'avatar': Mock.Random.image() },
            { 'userid': Mock.Random.id(), 'avatar': Mock.Random.image() }
          ]
        }))
      }
      return res
    }
    return Promise.resolve('123')
  }
  return request
})

fly.interceptors.response.use(
  (response) => {
    return response.data
  },
  (err) => {
    console.log(err)
  }
)

export default fly
