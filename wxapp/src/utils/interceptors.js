import config from '@/config'
import Mock from 'mockjs'

var Fly = require('flyio/dist/npm/wx')

var fly = new Fly()
let DEBUG = config.DEBUG
let host = config.host

fly.config.timeout = 10
fly.config.baseUrl = config.host

fly.interceptors.request.use((request) => {
  request.headers['X-Tag'] = 'flyio'
  if (DEBUG) {
    if (request.url === `${host}/users/123/activities`) {
      let res = []
      for (let i = 0; i < 20; i++) {
        res.push(Mock.mock({
          'id': Mock.Random.id(),
          'title': Mock.Random.csentence(4),
          'thumb': Mock.Random.image(),
          'description': Mock.Random.cparagraph(1),
          'content': Mock.Random.cparagraph(5),
          'time': Mock.Random.date(),
          'location': Mock.Random.county(),
          'leaderName': Mock.Random.cname(),
          'leaderID': Mock.Random.guid(),
          'type|1': ['applying', 'applyed', 'created', 'creating'],
          'members': [
            {'userid': Mock.Random.id(), 'avatar': Mock.Random.image()},
            {'userid': Mock.Random.id(), 'avatar': Mock.Random.image()}
          ]
        }))
      }
      return Promise.resolve(res)
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
