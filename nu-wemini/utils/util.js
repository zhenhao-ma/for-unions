import config from './config'
// General Utils
export function isDef(value) {
  return value !== null && value !== undefined
}
export function isUndef (value){
  return value === null || value === undefined
}
export function isTrue (value) {
  return value === true
}
export function isFalse(value) {
  return value === false
}

// Requests
export function get(url, data) {
  return request(url, 'GET', data)
}
export function post(url, data) {
  return request(url, 'POST', data)
}
function request(url, method, data) {
  const accessToken = wx.getStorageSync('accessToken')
  console.log('URL: ', config.API_PREFIX + url)
  return new Promise((resolve, reject) => {
    wx.request({
      header: {
        'Authorization': `Bearer ${accessToken}`
      },
      url: config.API_PREFIX + url,
      timeout: 10000,
      method,
      data,
      dataType: 'json',
      success: (res) => {
        resolve(res.data)
      },
      fail: (res) => {
        reject(res);
      }
    })
  })
}

// Reformat
export const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return `${[year, month, day].map(formatNumber).join('/')} ${[hour, minute, second].map(formatNumber).join(':')}`
}

export const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : `0${n}`
}
