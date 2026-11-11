package com.neu.llm.controller;

import java.util.List;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.github.xiaoymin.knife4j.annotations.DynamicParameter;
import com.github.xiaoymin.knife4j.annotations.DynamicResponseParameters;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import com.neu.common.annotation.Log;
import com.neu.common.core.controller.BaseController;
import com.neu.common.core.domain.AjaxResult;
import com.neu.common.enums.BusinessType;
import com.neu.llm.domain.SessionInformation;
import com.neu.llm.service.ISessionInformationService;
import com.neu.common.utils.poi.ExcelUtil;
import com.neu.common.core.page.TableDataInfo;

/**
 * session_informationController
 * 
 * @author neuedu
 * @date 2024-06-02
 */
@Api(tags = {"session_information"})
@RestController
@RequestMapping("/llm/session_information")
public class SessionInformationController extends BaseController
{
    @Autowired
    private ISessionInformationService sessionInformationService;

    /**
     * 查询session_information列表
     */
    @GetMapping("/list")
    @ApiOperation("查询session_information列表")
    @DynamicResponseParameters(properties = {
	        @DynamicParameter(name = "total", value = "总记录数"),
            @DynamicParameter(name = "code", value = "状态码，200正确，其他错误"),
            @DynamicParameter(name = "rows", value = "返回业务数据（数组类型）", dataTypeClass = SessionInformation.class),
            @DynamicParameter(name = "msg", value = "返回消息内容")
    })
    public TableDataInfo list(SessionInformation sessionInformation)
    {
        startPage();
        List<SessionInformation> list = sessionInformationService.selectSessionInformationList(sessionInformation);
        return getDataTable(list);
    }

    /**
     * 导出session_information列表
     */
    @ApiOperation("导出session_information列表")
    @DynamicResponseParameters(properties = {
            @DynamicParameter(name = "code", value = "状态码，200正确，其他错误"),
            @DynamicParameter(name = "msg", value = "文件名")
    })
    @PreAuthorize("@ss.hasPermi('llm:session_information:export')")
    @Log(title = "session_information", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(SessionInformation sessionInformation)
    {
        List<SessionInformation> list = sessionInformationService.selectSessionInformationList(sessionInformation);
        ExcelUtil<SessionInformation> util = new ExcelUtil<SessionInformation>(SessionInformation.class);
        return util.exportExcel(list, "session_information");
    }

    /**
     * 获取session_information详细信息
     */
    @ApiOperation("获取session_information详细信息")
    @DynamicResponseParameters(properties = {
            @DynamicParameter(name = "code", value = "状态码，200正确，其他错误"),
            @DynamicParameter(name = "data", value = "返回业务数据", dataTypeClass = SessionInformation.class),
            @DynamicParameter(name = "msg", value = "返回消息内容")
    })
    @GetMapping(value = "/{sessionId}")
    public AjaxResult getInfo(@PathVariable("sessionId") Long sessionId)
    {
        return AjaxResult.success(sessionInformationService.selectSessionInformationById(sessionId));
    }

    /**
     * 新增session_information
     */
    @ApiOperation("新增session_information")
    @DynamicResponseParameters(properties = {
            @DynamicParameter(name = "code", value = "状态码，200正确，其他错误"),
            @DynamicParameter(name = "msg", value = "返回消息内容")
    })
    @PreAuthorize("@ss.hasPermi('llm:session_information:add')")
    @Log(title = "session_information", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody SessionInformation sessionInformation)
    {
        return toAjax(sessionInformationService.insertSessionInformation(sessionInformation));
    }

    /**
     * 修改session_information
     */
    @ApiOperation("修改session_information")
    @DynamicResponseParameters(properties = {
            @DynamicParameter(name = "code", value = "状态码，200正确，其他错误"),
            @DynamicParameter(name = "msg", value = "返回消息内容")
    })
    @PreAuthorize("@ss.hasPermi('llm:session_information:edit')")
    @Log(title = "session_information", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody SessionInformation sessionInformation)
    {
        return toAjax(sessionInformationService.updateSessionInformation(sessionInformation));
    }

    /**
     * 删除session_information
     */
    @ApiOperation("删除session_information")
    @DynamicResponseParameters(properties = {
            @DynamicParameter(name = "code", value = "状态码，200正确，其他错误"),
            @DynamicParameter(name = "msg", value = "返回消息内容")
    })
    @PreAuthorize("@ss.hasPermi('llm:session_information:remove')")
    @Log(title = "session_information", businessType = BusinessType.DELETE)
	@DeleteMapping("/{sessionIds}")
    public AjaxResult remove(@PathVariable Long[] sessionIds)
    {
        return toAjax(sessionInformationService.deleteSessionInformationByIds(sessionIds));
    }
}
