<template>
  <div>
    <ve-line 
      :data="getChartData()"
      :toolbox="toolbox"
      :colors="colors"
      :settings="chartSettings"
       :extend="extend"
    ></ve-line>
    <el-row>
      <el-table
        :data="productResults"
        stripe
        style="width: 100%">
        <el-table-column
          prop="productId"
          label="商品id"
          width="180">
        </el-table-column>
        <el-table-column
          align="center"
          prop="name"
          label="名称"
          min-width="120">
        </el-table-column>
        <el-table-column
          align="left"
          label="链接">
          <template slot-scope="scope">
            <i class="el-icon-share"></i>
            <a :href="`https://item.jd.com/${scope.row.productId}.html#comment`"
              target="_blank"
              >  {{scope.row.name}} </a>
          </template>
        </el-table-column>
      </el-table>
      
    </el-row>

    <el-row v-for="item in productResults"  v-bind:key="item.id">
       <!-- <el-divider content-position="left">{{item.name}}</el-divider>
       -->
      <el-col :span="12">
        <el-row v-for="(comments, name) in item.comment"  v-bind:key="comments.id">
          <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item >{{item.name}}</el-breadcrumb-item>
            <el-breadcrumb-item>{{name}}</el-breadcrumb-item>
          </el-breadcrumb>
          <ve-wordcloud 
            :data="getComments(comments).cloudData"
            :settings="cloudSettings"
            ></ve-wordcloud>
          <el-tooltip placement="top">
            <div slot="content" v-for="s in getComments(comments).words" v-bind:key="s.id">{{s}}</div>
            <el-button>🖱鼠标滑到这里看看->{{name}}</el-button>
          </el-tooltip>
        </el-row>
      </el-col>

      <el-col :span="12">
        <ve-pie 
        :data="getPieData(item)"
        :colors="colors"
        ></ve-pie>
      </el-col>

    </el-row>
    <el-pagination
      @next-click="nextPage"
      @prev-click="prevPage"
      @current-change="changePage"
      background
      layout="prev, pager, next"
      :total="total">
    </el-pagination>
  </div>
</template>

<script>

import axios from 'axios'
// const host = 'http://server:5000'
const resultsApi = '/api/v1/results'


export default {
  data () {
    this.toolbox = {
        feature: {
          magicType: {type: ['line', 'bar']},
          saveAsImage: {}
        }
      }
      this.extend = {
        'xAxis.0.axisLabel.rotate': 45,
        series: {
          label: {
            normal: {
              show: true
            }
          }
        }
      }
      this.colors = ['#409EFF','#67C23A', '#E6A23C', '#d48265', '#F56C6C', '#909399']
      // 叠加柱状图
      this.chartSettings = {
        axisSite: { right: ['poorRate'] },
        yAxisType: ['normal', 'percent'],
        yAxisName: ['评论数', '差评率'],
        dataType: {
          // '访问用户': 'KMB',
          // '年龄': 'percent',
          'poorCount': 'normal'
        },
        labelMap: {
          commentCount: '评论总数',
          poorCount: '差评数',
          poorRate: '差评率'
        },
        // stack: { '1': ['commentCount', 'poorCount'] }
      }
      this.cloudSettings = {
        shape: 'star'
      }
    return {
        productResults: [],
        sumResults: [],
        total: 0,
        nextUrl: '',
        prevUrl: ''
    }
  },
    created() {
      this.get_result(resultsApi)
      this.get_result(resultsApi, 'sum')
    },
    methods: {
      get_result(url, key='') {
        const urlParams = this.$route.query;
        // console.log(urlParams);
        let currentToken = urlParams.token;
        axios.get(url, {
            params: {
              token: currentToken ? currentToken : sessionStorage.getItem('token'),
              key
            }
          }).then(res =>{
            // console.log(res.data);
            if (key) {
              this.sumResults = res.data.results
            } else {
              this.productResults = res.data.results
              }
            this.total = res.data.count
            this.nextUrl = res.data.next
            this.prevUrl = res.data.previous
          }).catch(err=>{
            console.log(err);
          })
      },
      nextPage(page) {
        console.log('[nextPage]', page);
        // let url = this.nextUrl
        this.get_result(this.nextUrl)
        this.get_result(this.nextUrl, 'sum')
      },
      prevPage(page) {
        console.log('[prevPage]', page);
        this.get_result(this.prevUrl)
        this.get_result(this.prevUrl, 'sum')
      },
      changePage(page){
        console.log('[changePage]', page);
        // page=2, -> /api/v1/results?start=11&limit=10
        // string to int
        let startPage = (parseInt(page)-1)*10+1
        // console.log(startPage, page);
        let url = '/api/v1/results?start=' + startPage + '&limit=10'
        this.get_result(url)
        this.get_result(url, 'sum')
      },
      // 动态加载每一个产品
      getChartData() {
        let chartData =  {
            columns: ['productId', 'commentCount', 'poorCount', 'poorRate'],
            rows: []
          }
        if (this.productResults.length){
          for (var i in this.productResults){
            let result = this.productResults[i]
            let comm = this.sumResults[i]
            // console.log(comm)
            if (comm) {
              chartData.rows.push({
                productId: comm.productId.toString() + '-' + result.name.slice(0,10),  // for short
                commentCount: comm.commentCount,
                poorCount: comm.poorCount,
                poorRate: comm.poorRate
              })
            }
          }
        }
        return chartData
      },
      getPieData(item){
          let pieData = {
          columns: ['productColor', 'count'],
          rows: []
        }
        for (var i in item.color) {
          let row = {}
          row.productColor = i
          row.count = item.color[i]
          pieData.rows.push(row)
        }
        return pieData
      },
            
      getComments(comments) {
        let cloudData = {
          columns: ['word', 'count'],
          rows: []
        }
        let words = []
        for(var k in comments){
          // console.log(k, comments[k].length, comments[k])
          cloudData.rows.push({
            'word': k,
            'count': comments[k].length
          })
          words = words.concat(comments[k])
        }
        // console.log(cloudData.rows, words);
          return {
            cloudData,
            words
          }
        }
    }
}
</script>

<style scoped lang="scss">
  .box {
    width: 300px;
    height: 400px;
    .top {
      text-align: center;
    }

    .left {
      float: left;
      width: 60px;
    }

    .right {
      float: right;
      width: 60px;
    }

    .bottom {
      clear: both;
      text-align: center;
    }

    .item {
      margin: 4px;
    }

    .left .el-tooltip__popper,
    .right .el-tooltip__popper {
      padding: 8px 10px;
    }
  }
</style>