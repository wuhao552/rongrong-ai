package com.neu.media.service;

import java.util.List;
import com.neu.media.domain.Video;

/**
 * videoService接口
 * 
 * @author neuedu
 * @date 2024-06-30
 */
public interface IVideoService 
{
    /**
     * 查询video
     * 
     * @param id videoID
     * @return video
     */
    public Video selectVideoById(Long id);

    /**
     * 查询video列表
     * 
     * @param video video
     * @return video集合
     */
    public List<Video> selectVideoList(Video video);

    /**
     * 新增video
     * 
     * @param video video
     * @return 结果
     */
    public int insertVideo(Video video);

    /**
     * 修改video
     * 
     * @param video video
     * @return 结果
     */
    public int updateVideo(Video video);

    /**
     * 批量删除video
     * 
     * @param ids 需要删除的videoID
     * @return 结果
     */
    public int deleteVideoByIds(Long[] ids);

    /**
     * 删除video信息
     * 
     * @param id videoID
     * @return 结果
     */
    public int deleteVideoById(Long id);
}
