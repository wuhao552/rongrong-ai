package com.neu.llm.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.neu.llm.mapper.SessionInformationMapper;
import com.neu.llm.domain.SessionInformation;
import com.neu.llm.service.ISessionInformationService;

/**
 * session_informationService业务层处理
 * 
 * @author neuedu
 * @date 2024-06-02
 */
@Service
public class SessionInformationServiceImpl implements ISessionInformationService 
{
    @Autowired
    private SessionInformationMapper sessionInformationMapper;

    /**
     * 查询session_information
     * 
     * @param sessionId session_informationID
     * @return session_information
     */
    @Override
    public SessionInformation selectSessionInformationById(Long sessionId)
    {
        return sessionInformationMapper.selectSessionInformationById(sessionId);
    }

    /**
     * 查询session_information列表
     * 
     * @param sessionInformation session_information
     * @return session_information
     */
    @Override
    public List<SessionInformation> selectSessionInformationList(SessionInformation sessionInformation)
    {
        return sessionInformationMapper.selectSessionInformationList(sessionInformation);
    }

    /**
     * 新增session_information
     * 
     * @param sessionInformation session_information
     * @return 结果
     */
    @Override
    public int insertSessionInformation(SessionInformation sessionInformation)
    {
        return sessionInformationMapper.insertSessionInformation(sessionInformation);
    }

    /**
     * 修改session_information
     * 
     * @param sessionInformation session_information
     * @return 结果
     */
    @Override
    public int updateSessionInformation(SessionInformation sessionInformation)
    {
        return sessionInformationMapper.updateSessionInformation(sessionInformation);
    }

    /**
     * 批量删除session_information
     * 
     * @param sessionIds 需要删除的session_informationID
     * @return 结果
     */
    @Override
    public int deleteSessionInformationByIds(Long[] sessionIds)
    {
        return sessionInformationMapper.deleteSessionInformationByIds(sessionIds);
    }

    /**
     * 删除session_information信息
     * 
     * @param sessionId session_informationID
     * @return 结果
     */
    @Override
    public int deleteSessionInformationById(Long sessionId)
    {
        return sessionInformationMapper.deleteSessionInformationById(sessionId);
    }
}
