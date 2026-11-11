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
 * session_information对象 session_information
 * 
 * @author neuedu
 * @date 2024-06-02
 */
@ApiModel("session_information")
public class SessionInformation extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 对话会话ID */
    @ApiModelProperty("对话会话ID")
    private Long sessionId;

    /** 用户ID */
    @ApiModelProperty("用户ID")
    @Excel(name = "用户ID")
    private Long userId;

    /** 会话创建时间 */
    @ApiModelProperty(value="会话创建时间",example = "2021-09-10")
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "会话创建时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date createdAt;

    /** 对话状态 */
    @ApiModelProperty("对话状态")
    @Excel(name = "对话状态")
    private String sessionStatus;

    public void setSessionId(Long sessionId) 
    {
        this.sessionId = sessionId;
    }

    public Long getSessionId() 
    {
        return sessionId;
    }
    public void setUserId(Long userId) 
    {
        this.userId = userId;
    }

    public Long getUserId() 
    {
        return userId;
    }
    public void setCreatedAt(Date createdAt) 
    {
        this.createdAt = createdAt;
    }

    public Date getCreatedAt() 
    {
        return createdAt;
    }
    public void setSessionStatus(String sessionStatus) 
    {
        this.sessionStatus = sessionStatus;
    }

    public String getSessionStatus() 
    {
        return sessionStatus;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("sessionId", getSessionId())
            .append("userId", getUserId())
            .append("createdAt", getCreatedAt())
            .append("sessionStatus", getSessionStatus())
            .toString();
    }
}
