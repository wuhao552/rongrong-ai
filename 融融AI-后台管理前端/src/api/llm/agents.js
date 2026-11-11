import request from '@/utils/request'

// 查询agents列表
export function listAgents(query) {
  return request({
    url: '/llm/agents/list',
    method: 'get',
    params: query
  })
}

// 查询agents详细
export function getAgents(agentId) {
  return request({
    url: '/llm/agents/' + agentId,
    method: 'get'
  })
}

// 新增agents
export function addAgents(data) {
  return request({
    url: '/llm/agents',
    method: 'post',
    data: data
  })
}

// 修改agents
export function updateAgents(data) {
  return request({
    url: '/llm/agents',
    method: 'put',
    data: data
  })
}

// 删除agents
export function delAgents(agentId) {
  return request({
    url: '/llm/agents/' + agentId,
    method: 'delete'
  })
}

// 导出agents
export function exportAgents(query) {
  return request({
    url: '/llm/agents/export',
    method: 'get',
    params: query
  })
}