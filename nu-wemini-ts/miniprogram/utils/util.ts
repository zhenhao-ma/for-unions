// General Utils
export function isDef(value: unknown): boolean {
  return value !== null && value !== undefined
}
export function isUndef (value: unknown): boolean {
  return value === null || value === undefined
}
export function isTrue (value: unknown): boolean {
  return value === true
}
export function isFalse(value: unknown): boolean {
  return value === false
}

export const formatTime = (date: Date): string => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return (
    [year, month, day].map(formatNumber).join('/') +
    ' ' +
    [hour, minute, second].map(formatNumber).join(':')
  )
}

const formatNumber = (n: number): string => {
  const s = n.toString()
  return s[1] ? s : '0' + s
}
