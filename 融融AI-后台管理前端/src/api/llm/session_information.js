import request from '@/utils/request'

// 查询session_information列表
export function listSession_information(query) {
  return request({
    url: '/llm/session_information/list',
    method: 'get',
    params: query
  })
}

// 查询session_information详细
export function getSession_information(sessionId) {
  return request({
    url: '/llm/session_information/' + sessionId,
    method: 'get'
  })
}

// 新增session_information
export function addSession_information(data) {
  return request({
    url: '/llm/session_information',
    method: 'post',
    data: data
  })
}

// 修改session_information
export function updateSession_information(data) {
  return request({
    url: '/llm/session_information',
    method: 'put',
    data: data
  })
}

// 删除session_information
export function delSession_information(sessionId) {
  return request({
    url: '/llm/session_information/' + sessionId,
    method: 'delete'
  })
}

// 导出session_information
export function exportSession_information(query) {
  return request({
    url: '/llm/session_information/export',
    method: 'get',
    params: query
  })
}