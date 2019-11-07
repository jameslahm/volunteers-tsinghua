import fly from '@/utils/interceptors'
import config from '@/config'

let host = config.host

export const get = (params) => {
  return fly.get(`${host}${params.url}`, params.data)
}

export const post = (params) => {
  return fly.post(`${host}${params.url}`, params.data)
}
