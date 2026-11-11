package com.neu.llm.service;

import java.util.List;
import com.neu.llm.domain.Agents;

/**
 * agentsService接口
 * 
 * @author neuedu
 * @date 2024-07-03
 */
public interface IAgentsService 
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
     * 批量删除agents
     * 
     * @param agentIds 需要删除的agentsID
     * @return 结果
     */
    public int deleteAgentsByIds(Long[] agentIds);

    /**
     * 删除agents信息
     * 
     * @param agentId agentsID
     * @return 结果
     */
    public int deleteAgentsById(Long agentId);
}
