<template>
  <div class="analysis">
    <h1>数据分析可视化</h1>
    <ve-line 
      :data="chartData"
      :toolbox="toolbox"
      :settings="chartSettings"
      ></ve-line>

      <el-row v-for="item in 5" :key="item.id">
        <el-col :span="12">
          <ve-wordcloud 
            :data="cloudData"
            :settings="cloudSettings"
            ></ve-wordcloud>
        </el-col>
        <el-col :span="12">
          <ve-pie :data="pieData"></ve-pie>
        </el-col>

      </el-row>
  </div>
</template>


<script>
  export default {
    data: function () {
      this.toolbox = {
        feature: {
          magicType: {type: ['line', 'bar']},
          saveAsImage: {}
        }
      }
      this.chartSettings = {
        stack: { '用户': ['访问用户', '下单用户'] }
      }
      this.cloudSettings = {
        shape: 'star'
      }
      return {
        chartData: {
          columns: ['日期', '访问用户', '下单用户', '下单率'],
          rows: [
            { '日期': '1/1', '访问用户': 1393, '下单用户': 1093, '下单率': 0.32 },
            { '日期': '1/2', '访问用户': 3530, '下单用户': 3230, '下单率': 0.26 },
            { '日期': '1/3', '访问用户': 2923, '下单用户': 2623, '下单率': 0.76 },
            { '日期': '1/4', '访问用户': 1723, '下单用户': 1423, '下单率': 0.49 },
            { '日期': '1/5', '访问用户': 3792, '下单用户': 3492, '下单率': 0.323 },
            { '日期': '1/6', '访问用户': 4593, '下单用户': 4293, '下单率': 0.78 }
          ]
        },
        pieData: {
          columns: ['日期', '访问用户'],
          rows: [
            { '日期': '1/1', '访问用户': 1393 },
            { '日期': '1/2', '访问用户': 3530 },
            { '日期': '1/3', '访问用户': 2923 },
            { '日期': '1/4', '访问用户': 1723 },
            { '日期': '1/5', '访问用户': 3792 },
            { '日期': '1/6', '访问用户': 4593 }
          ]
        },
        cloudData: {
          columns: ['word', 'count'],
          rows: this.getRows()
        }
      }
    },
    methods: {
      getRows () {
          return [{
            'word': 'visualMap',
            'count': 22199
          }, {
            'word': 'continuous',
            'count': 10288
          }, {
            'word': 'contoller',
            'count': 620
          }, {
            'word': 'series',
            'count': 274470
          }, {
            'word': 'gauge',
            'count': 12311
          }, {
            'word': 'detail',
            'count': 1206
          }, {
            'word': 'piecewise',
            'count': 4885
          }, {
            'word': 'textStyle',
            'count': 32294
          }, {
            'word': 'markPoint',
            'count': 18574
          }, {
            'word': 'pie',
            'count': 38929
          }, {
            'word': 'roseType',
            'count': 969
          }, {
            'word': 'label',
            'count': 37517
          }, {
            'word': 'emphasis',
            'count': 12053
          }, {
            'word': 'yAxis',
            'count': 57299
          }, {
            'word': 'name',
            'count': 15418
          }, {
            'word': 'type',
            'count': 22905
          }, {
            'word': 'gridIndex',
            'count': 5146
          }, {
            'word': 'normal',
            'count': 49487
          }, {
            'word': 'itemStyle',
            'count': 33837
          }, {
            'word': 'min',
            'count': 4500
          }, {
            'word': 'silent',
            'count': 5744
          }, {
            'word': 'animation',
            'count': 4840
          }, {
            'word': 'offsetCenter',
            'count': 232
          }, {
            'word': 'inverse',
            'count': 3706
          }, {
            'word': 'borderColor',
            'count': 4812
          }, {
            'word': 'markLine',
            'count': 16578
          }, {
            'word': 'line',
            'count': 76970
          }, {
            'word': 'radiusAxis',
            'count': 6704
          }, {
            'word': 'radar',
            'count': 15964
          }, {
            'word': 'data',
            'count': 60679
          }, {
            'word': 'dataZoom',
            'count': 24347
          }, {
            'word': 'tooltip',
            'count': 43420
          }, {
            'word': 'toolbox',
            'count': 25222
          }, {
            'word': 'geo',
            'count': 16904
          }, {
            'word': 'parallelAxis',
            'count': 4029
          }]
        }
    }

  }
</script>