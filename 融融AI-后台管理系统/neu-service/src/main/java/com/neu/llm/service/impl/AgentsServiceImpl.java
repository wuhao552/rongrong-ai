package com.neu.llm.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.neu.llm.mapper.AgentsMapper;
import com.neu.llm.domain.Agents;
import com.neu.llm.service.IAgentsService;

/**
 * agentsService业务层处理
 * 
 * @author neuedu
 * @date 2024-07-03
 */
@Service
public class AgentsServiceImpl implements IAgentsService 
{
    @Autowired
    private AgentsMapper agentsMapper;

    /**
     * 查询agents
     * 
     * @param agentId agentsID
     * @return agents
     */
    @Override
    public Agents selectAgentsById(Long agentId)
    {
        return agentsMapper.selectAgentsById(agentId);
    }

    /**
     * 查询agents列表
     * 
     * @param agents agents
     * @return agents
     */
    @Override
    public List<Agents> selectAgentsList(Agents agents)
    {
        return agentsMapper.selectAgentsList(agents);
    }

    /**
     * 新增agents
     * 
     * @param agents agents
     * @return 结果
     */
    @Override
    public int insertAgents(Agents agents)
    {
        return agentsMapper.insertAgents(agents);
    }

    /**
     * 修改agents
     * 
     * @param agents agents
     * @return 结果
     */
    @Override
    public int updateAgents(Agents agents)
    {
        return agentsMapper.updateAgents(agents);
    }

    /**
     * 批量删除agents
     * 
     * @param agentIds 需要删除的agentsID
     * @return 结果
     */
    @Override
    public int deleteAgentsByIds(Long[] agentIds)
    {
        return agentsMapper.deleteAgentsByIds(agentIds);
    }

    /**
     * 删除agents信息
     * 
     * @param agentId agentsID
     * @return 结果
     */
    @Override
    public int deleteAgentsById(Long agentId)
    {
        return agentsMapper.deleteAgentsById(agentId);
    }
}
