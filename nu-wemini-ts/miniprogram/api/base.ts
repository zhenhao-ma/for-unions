import { config } from "../config"

// Requests
export function get<T>(url: Url, data: unknown = undefined): Promise<T> {
  return request<T>(url, 'GET', data as RequestData)
}
export function post<T>(url: Url, data: unknown = undefined): Promise<T> {
  return request<T>(url, 'POST', data as RequestData)
}
export function put<T>(url: Url, data: unknown = undefined): Promise<T> {
  return request<T>(url, 'PUT', data as RequestData)
}
function request<T>(url: Url, method: 'GET' | 'POST' | 'DELETE' | 'PUT', data: RequestData): Promise<T> {
  const accessToken = wx.getStorageSync('accessToken')
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
        resolve(res.data as T)
      },
      fail: (res) => {
        reject(res);
      }
    })
  })
}
