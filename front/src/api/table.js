import request from '@/utils/request'

export function list(params) {
  return request({
    url: '/api/ssr/list',
    method: 'get'
  })
}

export function remove(data) {
  return request({
    url: '/api/ssr/delete',
    method: 'post',
    data: data
  })
}

export function add(data) {
  return request({
    url: '/api/ssr/add',
    method: 'post',
    data: data
  })
}