<template>
    <div class="step">
        <el-steps :active="currentStep" align-center >
          <el-step title="步骤1" icon="el-icon-edit" description="创建任务"></el-step>
          <el-step title="步骤2" icon="el-icon-upload" description="任务爬取"></el-step>
          <el-step title="步骤3" icon="el-icon-picture" description="数据分析"></el-step>
        </el-steps>
    </div>
</template>


<script>
export default {
    name: 'step',
    props: {
        currentStep: Number
    }
}
</script>


