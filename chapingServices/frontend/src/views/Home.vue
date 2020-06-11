<template>
  <div class="home">
    <el-container>
      <el-header>
        <i class="el-icon-s-data"></i>
        <div class="header-title">
          <a href="/">差评分析助手</a>
        </div>
        <div class="header-tips">----从差评中挑选能忍的选项，为购物增加一丝理性的气息</div>
        
      </el-header>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="18" :offset="3">
            <Step :currentStep="currentStep"></Step>
            <el-card class="box-card">
              <Task v-if="currentStep==1"></Task>
              <Crawler v-if="currentStep==2"></Crawler>
              <Analysis v-if="currentStep==3"></Analysis>
            </el-card>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="6" :offset="5" class="home-desc">
            <p>
              <br>
              此网站为DE8UG教学项目，真实在线演示，将根据实际需求进行修改与更新。
            </p>
            <p>支持平台：京东，...</p>
            <br>
            <p>
              请按提示操作。感谢关注，Thanks♪(･ω･)ﾉ
            </p>
            <br>
            <p>
              回复【邀请码】，获取邀请码; 
               <br>              
              回复【差评】，获取详细信息
            </p>
            <input v-model="de8ugtoken" class='de8ugtoken' placeholder="输入邀请码">
            <el-button @click="addDe8ugToken(de8ugtoken)">提交</el-button>
          </el-col>
          <el-col :span="6">
            <img src="python随身听公众号.jpg" alt="DE8UG的公众号：Python随身听">
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { mapMutations } from "vuex";
      
// @ is an alias to /src
// import Step from '@/components/Step.vue'
// import Task from '@/components/Task.vue'
// import Crawler from '@/components/Crawler.vue'
// import Analysis from '@/components/Analysis.vue'

export default {
  name: 'home',
  components: {
    // Step,
    // Task,
    // Crawler,
    // Analysis
    'Step': ()=>import('@/components/Step.vue'),
    'Task': ()=>import('@/components/Task.vue'),
    'Crawler': ()=>import('@/components/Crawler.vue'),
    'Analysis': ()=>import('@/components/Analysis.vue')
  },
  data() {
    let sessionToken = sessionStorage.getItem("de8ugtoken")
    return {
      de8ugtoken: sessionToken ? sessionToken : ''
    }
  },
  created() {
    const urlParams = this.$route.query;
    // console.log(urlParams);
    let step = urlParams.changeStep? urlParams.changeStep : 1
    this.$store.dispatch('changeStep', parseInt(step))
  },
  watch: { // watch的第一种写法
    $route (to, from) {
        // console.log(this.currentStep)
        console.log('watch 👀', to, to.query)
        if (to.query.changeStep > 0) {
          this.$store.dispatch('changeStep', parseInt(to.query.changeStep))
        } else {
          this.$store.dispatch('changeStep', 1)
        }
        // console.log('>>from', from)
        // console.log(this.currentStep)
    }
  },
  computed: {
    ...mapState([
      'currentStep',
      // 'de8ugtoken'
    ])
  },
  methods: {
    ...mapMutations([
        'addDe8ugToken'
      ]),
  }
}
</script>

<style>
.el-header{
  display: flex;
  align-items: center;
  /* background-color: #edb053; */
  border-bottom: 1px solid gray;
  color: #fff;
  font-size: 30px;

background: #005AA7;  /* fallback for old browsers */
background: -webkit-linear-gradient(to left, rgb(138, 209, 233), #005AA7);  /* Chrome 10-25, Safari 5.1-6 */
background: linear-gradient(to left, rgb(138, 209, 233), #005AA7); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

 }
.el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }

  .el-card{
    margin-top: 50px;
  }

  .header-title {
    margin-left: 10px;
  }
  .header-title a{
    color: white;
    text-decoration: none;
  }

  .header-tips {
    margin-left: 30px;
    font-size: 20px;
  }

  .home-desc {
    text-align: left
  }

  .de8ugtoken {
    width: 120px;
    height: 38px;
    border: 1px dashed red;
  }

</style>

