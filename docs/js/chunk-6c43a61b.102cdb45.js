(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-6c43a61b"],{2686:function(t,e,a){"use strict";a.r(e);var n=a("cebe"),s=a.n(n),r={data:function(){return{tableData:[],taskCount:sessionStorage.getItem("token-count"),percent:0,countSuccess:0,countFailed:0,currentToken:0}},created:function(){this.getData()},methods:{getData:function(){var t=this;this.timer=setInterval(function(){100!=t.percent?t.updateStatus():clearInterval(t.timer)},5e3),this.updateStatus()},destroyed:function(){clearInterval(this.timer)},updateStatus:function(){var t=this,e=this.$route.query;this.currentToken=e.token,s.a.get("/api/v1/status",{headers:{Authorization:"Token "+this.$store.state.de8ugtoken},params:{token:this.currentToken}}).then(function(e){t.tableData=e.data,t.countSuccess=t.tableData.filter(function(t){return t.status=100}).length,t.countFailed=e.data.length-t.countSuccess;var a=t.tableData.filter(function(t){return 1!=t.status}).length;t.percent=100*(a/t.taskCount).toFixed(2)}).catch(function(t){})},start:function(){this.$store.dispatch("changeStep",3);var t=this.$router.history.current.path;this.$router.push({path:t,query:{changeStep:3,token:this.currentToken}})},formatter:function(t){return t.status},filterTag:function(t,e){return e.statusText===t},filterHandler:function(t,e,a){return e[a.property]===t}}},l=(a("76a5"),a("2877")),u={components:{Table:Object(l.a)(r,function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("el-progress",{attrs:{"text-inside":!0,"stroke-width":26,percentage:t.percent}}),a("el-row",[a("el-col",{attrs:{span:2}},[a("el-badge",{staticClass:"item",attrs:{value:t.countSuccess,max:99}},[a("el-button",{attrs:{size:"small",type:"success"}},[t._v("成功")])],1)],1),a("el-col",{attrs:{span:2}},[a("el-badge",{staticClass:"item",attrs:{value:t.countFailed,max:10}},[a("el-button",{attrs:{size:"small",type:"danger"}},[t._v("失败")])],1)],1),a("el-col",{attrs:{span:4,offset:16}},[a("el-button",{attrs:{type:"warning",disabled:100!=t.percent},on:{click:t.start}},[t._v("开始分析")])],1)],1),a("el-table",{staticStyle:{width:"100%"},attrs:{data:t.tableData,stripe:""}},[a("el-table-column",{attrs:{prop:"_id",label:"id",width:"180"}}),a("el-table-column",{attrs:{align:"center",prop:"status",label:"状态值"}}),a("el-table-column",{attrs:{align:"left",prop:"statusText",label:"标签",width:"100",filters:[{text:"成功",value:"成功"},{text:"失败",value:"失败"}],"filter-method":t.filterTag,"filter-placement":"bottom-end"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("el-tag",{attrs:{type:"成功"===e.row.statusText?"success":"error","disable-transitions":""}},[t._v(t._s(e.row.statusText))])]}}])})],1)],1)},[],!1,null,null,null).exports}},o=Object(l.a)(u,function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"Crawler"},[a("h1",[t._v("任务爬取状态")]),a("Table")],1)},[],!1,null,null,null);e.default=o.exports},"76a5":function(t,e,a){"use strict";var n=a("dedf");a.n(n).a},dedf:function(t,e,a){}}]);