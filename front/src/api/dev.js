import request from '@/utils/request'

export function info(params) {
    return request({
      url: '/api/dev/info',
      method: 'get'
    })
}