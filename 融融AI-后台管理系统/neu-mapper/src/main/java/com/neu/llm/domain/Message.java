package com.neu.llm.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.neu.common.annotation.Excel;
import com.neu.common.core.domain.BaseEntity;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

/**
 * message对象 message
 * 
 * @author neuedu
 * @date 2024-06-02
 */
@ApiModel("message")
public class Message extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 消息id */
    @ApiModelProperty("消息id")
    private Long messageId;

    /** 对话会话id */
    @ApiModelProperty("对话会话id")
    @Excel(name = "对话会话id")
    private Long sessionId;

    /** 发送者 */
    @ApiModelProperty("发送者")
    @Excel(name = "发送者")
    private String sender;

    /** 消息内容 */
    @ApiModelProperty("消息内容")
    private String content;

    /** 发送时间 */
    @ApiModelProperty(value="发送时间",example = "2021-09-10")
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "发送时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date sendTime;

    /** 上下文信息 */
    @ApiModelProperty("上下文信息")
    private String context;

    public void setMessageId(Long messageId) 
    {
        this.messageId = messageId;
    }

    public Long getMessageId() 
    {
        return messageId;
    }
    public void setSessionId(Long sessionId) 
    {
        this.sessionId = sessionId;
    }

    public Long getSessionId() 
    {
        return sessionId;
    }
    public void setSender(String sender) 
    {
        this.sender = sender;
    }

    public String getSender() 
    {
        return sender;
    }
    public void setContent(String content) 
    {
        this.content = content;
    }

    public String getContent() 
    {
        return content;
    }
    public void setSendTime(Date sendTime) 
    {
        this.sendTime = sendTime;
    }

    public Date getSendTime() 
    {
        return sendTime;
    }
    public void setContext(String context) 
    {
        this.context = context;
    }

    public String getContext() 
    {
        return context;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("messageId", getMessageId())
            .append("sessionId", getSessionId())
            .append("sender", getSender())
            .append("content", getContent())
            .append("sendTime", getSendTime())
            .append("context", getContext())
            .toString();
    }
}
