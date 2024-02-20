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

export function query(params){
  return request({
    url: '/api/ssr/status',
    method: 'get',
    params: params
  })
}

export function update(data){
  return request({
    url: '/api/ssr/update',
    method: 'post',
    data: data
  })
}

export function start(data){
  return request({
    url: '/api/ssr/start',
    method: 'post',
    data: data
  })
}

export function stop(data){
  return request({
    url: '/api/ssr/stop',
    method: 'post',
    data: data
  })  
}