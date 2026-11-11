package com.neu.media.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.neu.common.annotation.Excel;
import com.neu.common.core.domain.BaseEntity;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

/**
 * video对象 video
 * 
 * @author neuedu
 * @date 2024-06-30
 */
@ApiModel("video")
public class Video extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 视频id */
    @ApiModelProperty("视频id")
    private Long id;

    /** 视频URL */
    @ApiModelProperty("视频URL")
    @Excel(name = "视频URL")
    private String videoUrl;

    /** 标题 */
    @ApiModelProperty("标题")
    @Excel(name = "标题")
    private String title;

    /** 描述 */
    @ApiModelProperty("描述")
    private String description;

    /** 缩略图URL */
    @ApiModelProperty("缩略图URL")
    @Excel(name = "缩略图URL")
    private String imageUrl;

    /** 真实视频URL */
    @ApiModelProperty("真实视频URL")
    @Excel(name = "真实视频URL")
    private String realUrl;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setVideoUrl(String videoUrl) 
    {
        this.videoUrl = videoUrl;
    }

    public String getVideoUrl() 
    {
        return videoUrl;
    }
    public void setTitle(String title) 
    {
        this.title = title;
    }

    public String getTitle() 
    {
        return title;
    }
    public void setDescription(String description) 
    {
        this.description = description;
    }

    public String getDescription() 
    {
        return description;
    }
    public void setImageUrl(String imageUrl) 
    {
        this.imageUrl = imageUrl;
    }

    public String getImageUrl() 
    {
        return imageUrl;
    }
    public void setRealUrl(String realUrl) 
    {
        this.realUrl = realUrl;
    }

    public String getRealUrl() 
    {
        return realUrl;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("videoUrl", getVideoUrl())
            .append("title", getTitle())
            .append("description", getDescription())
            .append("imageUrl", getImageUrl())
            .append("realUrl", getRealUrl())
            .toString();
    }
}
