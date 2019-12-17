import fly from '@/utils/interceptors'
import config from '@/config'

let host = config.host
let port = config.port

export const get = (params) => {
  return fly.get(`${host}${port}/api${params.url}`, params.data)
}

export const post = (params) => {
  return fly.post(`${host}${port}/api${params.url}`, params.data)
}
