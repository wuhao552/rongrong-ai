package com.neu.llm.mapper;

import java.util.List;
import com.neu.llm.domain.Agents;

/**
 * agentsMapper接口
 * 
 * @author neuedu
 * @date 2024-07-03
 */
public interface AgentsMapper 
{
    /**
     * 查询agents
     * 
     * @param agentId agentsID
     * @return agents
     */
    public Agents selectAgentsById(Long agentId);

    /**
     * 查询agents列表
     * 
     * @param agents agents
     * @return agents集合
     */
    public List<Agents> selectAgentsList(Agents agents);

    /**
     * 新增agents
     * 
     * @param agents agents
     * @return 结果
     */
    public int insertAgents(Agents agents);

    /**
     * 修改agents
     * 
     * @param agents agents
     * @return 结果
     */
    public int updateAgents(Agents agents);

    /**
     * 删除agents
     * 
     * @param agentId agentsID
     * @return 结果
     */
    public int deleteAgentsById(Long agentId);

    /**
     * 批量删除agents
     * 
     * @param agentIds 需要删除的数据ID
     * @return 结果
     */
    public int deleteAgentsByIds(Long[] agentIds);
}
