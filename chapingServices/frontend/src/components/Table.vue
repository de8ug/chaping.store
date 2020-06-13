<template>
    <div>
        <el-progress :text-inside="true" :stroke-width="26" :percentage="percent"></el-progress>

        <el-row>
            <el-col :span="2">
                <el-badge :value="countSuccess" :max="99" class="item">
                    <el-button size="small" type="success">成功</el-button>
                </el-badge>
            </el-col>
            <el-col :span="2">
                <el-badge :value="countFailed" :max="10" class="item">
                    <el-button size="small" type="danger">失败</el-button>
                </el-badge>
            </el-col>
            <el-col :span="4" :offset="16">
                <!-- <el-button @click="clearFilter">状态筛选</el-button> -->
                <el-button @click="start" type="warning" :disabled="percent!=100">开始分析</el-button>
                <!-- <el-button @click="start" type="warning">开始分析</el-button> -->
            </el-col>

        </el-row>
    <el-table
        :data="tableData"
        stripe
        style="width: 100%">
        
        <el-table-column
        prop="_id"
        label="商品id"
        width="180">
        </el-table-column>
        <el-table-column
        align="center"
        prop="status"
        label="状态值"
        :formatter="formatter"
        >
        </el-table-column>
        <el-table-column
        align="left"
        prop="statusText"
        label="标签"
        width="250"
        :filters="filterList"
        :filter-method="filterTag"
        filter-placement="bottom-end">
        <template slot-scope="scope">
            <el-tag
            :type="scope.row.statusText === '成功' ? 'success' : 'error'"
            disable-transitions>{{scope.row.statusText}}</el-tag>
        </template>
        </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "axios";
const statusApi = '/api/v1/status'


  export default {
    data() {
      return {
        tableData: [],
        filterList: [],
        taskCount: sessionStorage.getItem('token-count'),
        percent: 0,
        countSuccess: 0,
        countFailed: 0,
        currentToken: 0
      }
    },
    created() {
      // run the first time
      this.getData()  
    },

    methods: {
      getData() {
        this.timer = setInterval(() => {
          console.log('this.percent:', this.percent)
          if (this.percent != 100) {
            this.updateStatus();
            } else {
              clearInterval(this.timer)
            }
          }, 5000)
        this.updateStatus();  // make sure all update   
      },
      destroyed () {
          clearInterval(this.timer)
      },
      updateStatus() {
        const urlParams = this.$route.query;
        console.log(urlParams);
        this.currentToken = urlParams.token;
        axios.get(statusApi, {
          headers: {
              Authorization: 'Token ' + this.$store.state.de8ugtoken
          },
          params: {
            token: this.currentToken 
          }
        }).then(res => {
          console.log('get token status:', res.data);
          this.tableData = res.data
          this.countSuccess = this.tableData.filter(x => x.status==100).length
          this.countFailed = res.data.length - this.countSuccess
          // 进度条百分比，这时候给%前面的数字
          let counting = this.tableData.filter(x => x.status!=1).length
          this.percent = (counting / this.taskCount).toFixed(2) * 100
          // console.log(this.percent);
          
        }).catch(err => {
          console.log(err);
        })
        this.makeFilterList()
      },
      makeFilterList(){
        let tempList = []
        // [{ text: '成功', value: '成功' }, { text: '失败', value: '失败' }]
        for (let item of this.tableData) {
          tempList.push(item.statusText);
        }
        tempList = [...new Set(tempList)]
        tempList = tempList.filter((item)=>{
            return item !== '爬取中'
        });
        this.filterList = []  // clear first
        for (let item of tempList) {
          this.filterList.push({ text: item, value: item });
        }
      },
      start() {
        this.$store.dispatch('changeStep', 3)
        let path = this.$router.history.current.path;
        this.$router.push({ path, query: {'changeStep': 3, token: this.currentToken} });
      },
      // clearFilter() {
      //   this.$refs.filterTable.clearFilter();
      // },
      formatter(row) {
        return row.status.toString();
      },
      filterTag(value, row) {
        return row.statusText === value;
      },
      filterHandler(value, row, column) {
        const property = column['property'];
        return row[property] === value;
      }
    }
  }
</script>

<style>
    .el-progress{
        margin-top:30px;
        margin-bottom:30px;
    }
</style>
