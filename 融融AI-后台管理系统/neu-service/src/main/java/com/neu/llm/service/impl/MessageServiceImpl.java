package com.neu.llm.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.neu.llm.mapper.MessageMapper;
import com.neu.llm.domain.Message;
import com.neu.llm.service.IMessageService;

/**
 * messageService业务层处理
 * 
 * @author neuedu
 * @date 2024-06-02
 */
@Service
public class MessageServiceImpl implements IMessageService 
{
    @Autowired
    private MessageMapper messageMapper;

    /**
     * 查询message
     * 
     * @param messageId messageID
     * @return message
     */
    @Override
    public Message selectMessageById(Long messageId)
    {
        return messageMapper.selectMessageById(messageId);
    }

    /**
     * 查询message列表
     * 
     * @param message message
     * @return message
     */
    @Override
    public List<Message> selectMessageList(Message message)
    {
        return messageMapper.selectMessageList(message);
    }

    /**
     * 新增message
     * 
     * @param message message
     * @return 结果
     */
    @Override
    public int insertMessage(Message message)
    {
        return messageMapper.insertMessage(message);
    }

    /**
     * 修改message
     * 
     * @param message message
     * @return 结果
     */
    @Override
    public int updateMessage(Message message)
    {
        return messageMapper.updateMessage(message);
    }

    /**
     * 批量删除message
     * 
     * @param messageIds 需要删除的messageID
     * @return 结果
     */
    @Override
    public int deleteMessageByIds(Long[] messageIds)
    {
        return messageMapper.deleteMessageByIds(messageIds);
    }

    /**
     * 删除message信息
     * 
     * @param messageId messageID
     * @return 结果
     */
    @Override
    public int deleteMessageById(Long messageId)
    {
        return messageMapper.deleteMessageById(messageId);
    }
}
