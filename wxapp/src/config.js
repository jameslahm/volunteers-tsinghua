var DEBUG = false
let host
let port
if (DEBUG) {
  host = ''
  port = ':5000'
} else {
  host = ''
  port = ':443'
}

const appid = ''
const appSecret = ''

const config = {
  host,
  appid,
  appSecret,
  DEBUG: DEBUG,
  port
}

export default config
