package com.neu.llm.mapper;

import java.util.List;
import com.neu.llm.domain.Message;

/**
 * messageMapper接口
 * 
 * @author neuedu
 * @date 2024-06-02
 */
public interface MessageMapper 
{
    /**
     * 查询message
     * 
     * @param messageId messageID
     * @return message
     */
    public Message selectMessageById(Long messageId);

    /**
     * 查询message列表
     * 
     * @param message message
     * @return message集合
     */
    public List<Message> selectMessageList(Message message);

    /**
     * 新增message
     * 
     * @param message message
     * @return 结果
     */
    public int insertMessage(Message message);

    /**
     * 修改message
     * 
     * @param message message
     * @return 结果
     */
    public int updateMessage(Message message);

    /**
     * 删除message
     * 
     * @param messageId messageID
     * @return 结果
     */
    public int deleteMessageById(Long messageId);

    /**
     * 批量删除message
     * 
     * @param messageIds 需要删除的数据ID
     * @return 结果
     */
    public int deleteMessageByIds(Long[] messageIds);
}
