import request from '../utils/request'

export function calculateNetwork(data) {
  return request({
    url: '/api/network/calculate',
    method: 'post',
    data
  })
}

export function summarizeIps(data) {
  return request({
    url: '/api/ip/summary',
    method: 'post',
    data
  })
}

export function convertIp(data) {
  return request({
    url: '/api/ip/convert',
    method: 'post',
    data
  })
}

export function formatIp(data) {
  return request({
    url: '/api/ip/format',
    method: 'post',
    data
  })
}

export function divideSubnet(data) {
  return request({
    url: '/api/network/divide',
    method: 'post',
    data
  })
}

export function queryIpLocation(data) {
  return request({
    url: '/api/ip/location',
    method: 'post',
    data
  })
}

export function queryDns(data) {
  return request({
    url: '/api/dns/query',
    method: 'post',
    data
  })
} 