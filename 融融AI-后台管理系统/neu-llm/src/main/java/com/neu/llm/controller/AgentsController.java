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
import com.neu.llm.domain.Agents;
import com.neu.llm.service.IAgentsService;
import com.neu.common.utils.poi.ExcelUtil;
import com.neu.common.core.page.TableDataInfo;

/**
 * agentsController
 * 
 * @author neuedu
 * @date 2024-07-03
 */
@Api(tags = {"agents"})
@RestController
@RequestMapping("/llm/agents")
public class AgentsController extends BaseController
{
    @Autowired
    private IAgentsService agentsService;

    /**
     * 查询agents列表
     */
    @GetMapping("/list")
    @ApiOperation("查询agents列表")
    @DynamicResponseParameters(properties = {
	        @DynamicParameter(name = "total", value = "总记录数"),
            @DynamicParameter(name = "code", value = "状态码，200正确，其他错误"),
            @DynamicParameter(name = "rows", value = "返回业务数据（数组类型）", dataTypeClass = Agents.class),
            @DynamicParameter(name = "msg", value = "返回消息内容")
    })
    public TableDataInfo list(Agents agents)
    {
        startPage();
        List<Agents> list = agentsService.selectAgentsList(agents);
        return getDataTable(list);
    }

    /**
     * 导出agents列表
     */
    @ApiOperation("导出agents列表")
    @DynamicResponseParameters(properties = {
            @DynamicParameter(name = "code", value = "状态码，200正确，其他错误"),
            @DynamicParameter(name = "msg", value = "文件名")
    })
    @PreAuthorize("@ss.hasPermi('llm:agents:export')")
    @Log(title = "agents", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(Agents agents)
    {
        List<Agents> list = agentsService.selectAgentsList(agents);
        ExcelUtil<Agents> util = new ExcelUtil<Agents>(Agents.class);
        return util.exportExcel(list, "agents");
    }

    /**
     * 获取agents详细信息
     */
    @ApiOperation("获取agents详细信息")
    @DynamicResponseParameters(properties = {
            @DynamicParameter(name = "code", value = "状态码，200正确，其他错误"),
            @DynamicParameter(name = "data", value = "返回业务数据", dataTypeClass = Agents.class),
            @DynamicParameter(name = "msg", value = "返回消息内容")
    })
    @GetMapping(value = "/{agentId}")
    public AjaxResult getInfo(@PathVariable("agentId") Long agentId)
    {
        return AjaxResult.success(agentsService.selectAgentsById(agentId));
    }

    /**
     * 新增agents
     */
    @ApiOperation("新增agents")
    @DynamicResponseParameters(properties = {
            @DynamicParameter(name = "code", value = "状态码，200正确，其他错误"),
            @DynamicParameter(name = "msg", value = "返回消息内容")
    })
    @PreAuthorize("@ss.hasPermi('llm:agents:add')")
    @Log(title = "agents", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Agents agents)
    {
        return toAjax(agentsService.insertAgents(agents));
    }

    /**
     * 修改agents
     */
    @ApiOperation("修改agents")
    @DynamicResponseParameters(properties = {
            @DynamicParameter(name = "code", value = "状态码，200正确，其他错误"),
            @DynamicParameter(name = "msg", value = "返回消息内容")
    })
    @PreAuthorize("@ss.hasPermi('llm:agents:edit')")
    @Log(title = "agents", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Agents agents)
    {
        return toAjax(agentsService.updateAgents(agents));
    }

    /**
     * 删除agents
     */
    @ApiOperation("删除agents")
    @DynamicResponseParameters(properties = {
            @DynamicParameter(name = "code", value = "状态码，200正确，其他错误"),
            @DynamicParameter(name = "msg", value = "返回消息内容")
    })
    @PreAuthorize("@ss.hasPermi('llm:agents:remove')")
    @Log(title = "agents", businessType = BusinessType.DELETE)
	@DeleteMapping("/{agentIds}")
    public AjaxResult remove(@PathVariable Long[] agentIds)
    {
        return toAjax(agentsService.deleteAgentsByIds(agentIds));
    }
}
