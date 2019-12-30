var DEBUG = false
let host
let port
if (DEBUG) {
  host = 'http://127.0.0.1'
  port = ':5000'
} else {
  host = 'https://2019-a16.iterator-traits.com'
  port = ':443'
}

host = 'https://2019-a16.iterator-traits.com'
port = ''

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
