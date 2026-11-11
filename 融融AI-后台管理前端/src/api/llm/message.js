import request from '@/utils/request'

// 查询message列表
export function listMessage(query) {
  return request({
    url: '/llm/message/list',
    method: 'get',
    params: query
  })
}

// 查询message详细
export function getMessage(messageId) {
  return request({
    url: '/llm/message/' + messageId,
    method: 'get'
  })
}

// 新增message
export function addMessage(data) {
  return request({
    url: '/llm/message',
    method: 'post',
    data: data
  })
}

// 修改message
export function updateMessage(data) {
  return request({
    url: '/llm/message',
    method: 'put',
    data: data
  })
}

// 删除message
export function delMessage(messageId) {
  return request({
    url: '/llm/message/' + messageId,
    method: 'delete'
  })
}

// 导出message
export function exportMessage(query) {
  return request({
    url: '/llm/message/export',
    method: 'get',
    params: query
  })
}