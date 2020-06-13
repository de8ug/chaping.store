<template>
  <div class="task">
        <el-row :gutter="20">
          <el-col :span="18" :offset="3">
              <h3>请从页面底部获取[邀请码]{{de8ugtoken}}，开启试用</h3>
          </el-col>
        </el-row>

        <el-row  v-if="de8ugtoken" class='hot'>热门搜索：
          <a v-for="hot in hotWords.slice(0,10)" :key="hot.id" :href="`/?changeStep=3&token=${hot.token}`" class='hot-a'>{{hot.words}}</a>
        </el-row>

      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="名称" prop="name">
          <el-input  v-model="ruleForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="url" prop="url">
          <el-input v-model="ruleForm.url"></el-input>
        </el-form-item>
        <div>提示：
          打开<a href="https://www.jd.com/allSort.aspx" target="_blank">京东的全部商品</a>，查看具体某一类商品链接，粘贴到url即可
        </div>
        <el-form-item  v-if="de8ugtoken">
          <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
      <div class="show" v-if="isShow">
        <p>
        任务创建成功，共{{currentTask.count}}个子任务，
        </p>
        <p>
          token:{{currentTask.token}}
        </p>
          <el-button type="primary" @click='start'>开始爬取</el-button>
      </div>
  </div>
</template>


<script>
import { mapState } from "vuex";

import axios from "axios";
// const taskApi = 'http://localhost:5000/api/v1/task'
// const statusApi = 'http://localhost:5000/api/v1/status'

const taskApi = '/api/v1/task'
const statusApi = '/api/v1/status'


  export default {
    data() {
      var checkUrl = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('不能为空'));
        } else{
          callback()
        }
      };
      var validateName = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入名称'));
        } else {
          callback();
        }
      };
      
      return {
        currentTask: {},
        isShow: false,
        hotWords: [],
        ruleForm: {
          name: '手机',
          url: 'https://list.jd.com/list.html?cat=9987,653,655&page=1&sort=sort_commentcount_desc&trans=1&JL=4_5_0#J_main'
        },
        rules: {
          name: [
            { validator: validateName, trigger: 'blur' }
          ],
          url: [
            { validator: checkUrl, trigger: 'blur' }
          ]
        }
      };
    },
    created() {
      console.log('de8ugtoken:', this.$store.state.de8ugtoken);
      this.getHotWords()
    },
    watch: {
      de8ugtoken() {
        console.log('changed: ', this.de8ugtoken)
        sessionStorage.setItem('de8ugtoken', this.de8ugtoken)
        this.getHotWords()
      }
    },
    computed: {
      ...mapState([
        'de8ugtoken'
        ])
      },
    methods: {
      getHotWords() {
          axios.get(statusApi, {
          headers: {
              Authorization: `Token ${this.de8ugtoken}`
          },
          params: { 
            token: 'hot'
          }
        }).then(res => {
          // console.log('get hot words:', res.data);
          this.hotWords = res.data
        }).catch(err => {
          console.log(err);
        })
      },
      createTask() {
        axios.post(taskApi, {
          url: this.ruleForm.url,
          name: this.ruleForm.name
        },{
          headers: {
            Authorization: 'Token ' + this.$store.state.de8ugtoken
          }
        }
        ).then(res => {
          console.log('[createTask]', res.data);
          if(res.data.status == 0){
            this.isShow = true
            this.currentTask.token = res.data.token
            this.currentTask.count = res.data.sku_list.length
            sessionStorage.setItem('token', res.data.token)
            this.$message({
              message: '恭喜你，' + res.data.statusText,
              type: 'success'
            });
          } else{
            this.isShow = false
            this.$message({
              message: res.data.statusText,
              type: 'error'
            });
          }
        }).catch(err => {
          console.log(err);
        })
      },
      start() {
        this.$store.dispatch('changeStep', 2)
        let path = this.$router.history.current.path;
        this.$router.push({ path, query: {'changeStep': 2, token: this.currentTask.token} });
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            // alert('submit!');
            // TODO: 
            this.createTask()
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
  }
</script>

<style scoped>
.hot {
  text-align: left;
  color: red;
}
.hot-a {
  margin-right: 15px;
}
</style>