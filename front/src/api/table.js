import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/api/ssr/list',
    method: 'get',
    params
  })
}
