package com.neu.media.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.neu.media.mapper.VideoMapper;
import com.neu.media.domain.Video;
import com.neu.media.service.IVideoService;

/**
 * videoService业务层处理
 * 
 * @author neuedu
 * @date 2024-06-30
 */
@Service
public class VideoServiceImpl implements IVideoService 
{
    @Autowired
    private VideoMapper videoMapper;

    /**
     * 查询video
     * 
     * @param id videoID
     * @return video
     */
    @Override
    public Video selectVideoById(Long id)
    {
        return videoMapper.selectVideoById(id);
    }

    /**
     * 查询video列表
     * 
     * @param video video
     * @return video
     */
    @Override
    public List<Video> selectVideoList(Video video)
    {
        return videoMapper.selectVideoList(video);
    }

    /**
     * 新增video
     * 
     * @param video video
     * @return 结果
     */
    @Override
    public int insertVideo(Video video)
    {
        return videoMapper.insertVideo(video);
    }

    /**
     * 修改video
     * 
     * @param video video
     * @return 结果
     */
    @Override
    public int updateVideo(Video video)
    {
        return videoMapper.updateVideo(video);
    }

    /**
     * 批量删除video
     * 
     * @param ids 需要删除的videoID
     * @return 结果
     */
    @Override
    public int deleteVideoByIds(Long[] ids)
    {
        return videoMapper.deleteVideoByIds(ids);
    }

    /**
     * 删除video信息
     * 
     * @param id videoID
     * @return 结果
     */
    @Override
    public int deleteVideoById(Long id)
    {
        return videoMapper.deleteVideoById(id);
    }
}
