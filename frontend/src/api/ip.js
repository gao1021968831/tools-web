import request from '../utils/request'

export function calculateNetwork(data) {
  return request({
    url: '/network/calculate',
    method: 'post',
    data
  })
}

export function summarizeIps(data) {
  return request({
    url: '/ip/summary',
    method: 'post',
    data
  })
}

export function convertIp(data) {
  return request({
    url: '/ip/convert',
    method: 'post',
    data
  })
}

export function formatIp(data) {
  return request({
    url: '/ip/format',
    method: 'post',
    data
  })
} 