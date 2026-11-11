package com.neu.llm.service;

import java.util.List;
import com.neu.llm.domain.SessionInformation;

/**
 * session_informationService接口
 * 
 * @author neuedu
 * @date 2024-06-02
 */
public interface ISessionInformationService 
{
    /**
     * 查询session_information
     * 
     * @param sessionId session_informationID
     * @return session_information
     */
    public SessionInformation selectSessionInformationById(Long sessionId);

    /**
     * 查询session_information列表
     * 
     * @param sessionInformation session_information
     * @return session_information集合
     */
    public List<SessionInformation> selectSessionInformationList(SessionInformation sessionInformation);

    /**
     * 新增session_information
     * 
     * @param sessionInformation session_information
     * @return 结果
     */
    public int insertSessionInformation(SessionInformation sessionInformation);

    /**
     * 修改session_information
     * 
     * @param sessionInformation session_information
     * @return 结果
     */
    public int updateSessionInformation(SessionInformation sessionInformation);

    /**
     * 批量删除session_information
     * 
     * @param sessionIds 需要删除的session_informationID
     * @return 结果
     */
    public int deleteSessionInformationByIds(Long[] sessionIds);

    /**
     * 删除session_information信息
     * 
     * @param sessionId session_informationID
     * @return 结果
     */
    public int deleteSessionInformationById(Long sessionId);
}
