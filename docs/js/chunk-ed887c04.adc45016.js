(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-ed887c04"],{"0bfb":function(t,e,o){"use strict";var r=o("cb7c");t.exports=function(){var t=r(this),e="";return t.global&&(e+="g"),t.ignoreCase&&(e+="i"),t.multiline&&(e+="m"),t.unicode&&(e+="u"),t.sticky&&(e+="y"),e}},"0d5c":function(t,e,o){"use strict";var r=o("d9f9");o.n(r).a},"13fa":function(t,e,o){"use strict";o.r(e),o("7f7f"),o("6b54");var r=o("cebe"),n=o.n(r),s="/api/v1/results",a={data:function(){return this.toolbox={feature:{magicType:{type:["line","bar"]},saveAsImage:{}}},this.extend={"xAxis.0.axisLabel.rotate":45,series:{label:{normal:{show:!0}}}},this.colors=["#409EFF","#67C23A","#E6A23C","#d48265","#F56C6C","#909399"],this.chartSettings={axisSite:{right:["poorRate"]},yAxisType:["normal","percent"],yAxisName:["评论数","差评率"],dataType:{poorCount:"normal"},labelMap:{commentCount:"评论总数",poorCount:"差评数",poorRate:"差评率"}},this.cloudSettings={shape:"star"},{productResults:[],sumResults:[],total:0,nextUrl:"",prevUrl:""}},created:function(){this.get_result(s),this.get_result(s,"sum")},methods:{get_result:function(t,e){var o=this,r=1<arguments.length&&void 0!==e?e:"",s=this.$route.query.token;n.a.get(t,{params:{token:s||sessionStorage.getItem("token"),key:r}}).then(function(t){r?o.sumResults=t.data.results:o.productResults=t.data.results,o.total=t.data.count,o.nextUrl=t.data.next,o.prevUrl=t.data.previous}).catch(function(t){})},nextPage:function(){this.get_result(this.nextUrl),this.get_result(this.nextUrl,"sum")},prevPage:function(){this.get_result(this.prevUrl),this.get_result(this.prevUrl,"sum")},changePage:function(t){var e="/api/v1/results?start="+(10*(parseInt(t)-1)+1)+"&limit=10";this.get_result(e),this.get_result(e,"sum")},getChartData:function(){var t={columns:["productId","commentCount","poorCount","poorRate"],rows:[]};if(this.productResults.length)for(var e in this.productResults){var o=this.productResults[e],r=this.sumResults[e];"{}"!==JSON.stringify(r)&&t.rows.push({productId:r.productId.toString()+"-"+o.name.slice(0,10),commentCount:r.commentCount,poorCount:r.poorCount,poorRate:r.poorRate})}return t},getPieData:function(t){var e={columns:["productColor","count"],rows:[]};for(var o in t.color){var r={};r.productColor=o,r.count=t.color[o],e.rows.push(r)}return e},getComments:function(t){var e={columns:["word","count"],rows:[]},o=[];for(var r in t)e.rows.push({word:r,count:t[r].length}),o=o.concat(t[r]);return{cloudData:e,words:o}}}},u=(o("0d5c"),o("2877")),c=Object(u.a)(a,function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",[o("ve-line",{attrs:{data:t.getChartData(),toolbox:t.toolbox,colors:t.colors,settings:t.chartSettings,extend:t.extend}}),o("el-row",[o("el-table",{staticStyle:{width:"100%"},attrs:{data:t.productResults,stripe:""}},[o("el-table-column",{attrs:{prop:"productId",label:"商品id",width:"180"}}),o("el-table-column",{attrs:{align:"center",prop:"name",label:"名称","min-width":"120"}}),o("el-table-column",{attrs:{align:"left",label:"链接"},scopedSlots:t._u([{key:"default",fn:function(e){return[o("i",{staticClass:"el-icon-share"}),o("a",{attrs:{href:"https://item.jd.com/"+e.row.productId+".html#comment",target:"_blank"}},[t._v("  "+t._s(e.row.name)+" ")])]}}])})],1)],1),t._l(t.productResults,function(e){return o("el-row",{key:e.id},[o("el-col",{attrs:{span:12}},t._l(e.comment,function(r,n){return o("el-row",{key:r.id},[o("el-breadcrumb",{attrs:{"separator-class":"el-icon-arrow-right"}},[o("el-breadcrumb-item",[t._v(t._s(e.name))]),o("el-breadcrumb-item",[t._v(t._s(n))])],1),o("ve-wordcloud",{attrs:{data:t.getComments(r).cloudData,settings:t.cloudSettings}}),o("el-tooltip",{attrs:{placement:"top"}},[t._l(t.getComments(r).words,function(e){return o("div",{key:e.id,attrs:{slot:"content"},slot:"content"},[t._v(t._s(e))])}),o("el-button",[t._v("🖱鼠标滑到这里看看->"+t._s(n))])],2)],1)}),1),o("el-col",{attrs:{span:12}},[o("ve-pie",{attrs:{data:t.getPieData(e),colors:t.colors}})],1)],1)}),o("el-pagination",{attrs:{background:"",layout:"prev, pager, next",total:t.total},on:{"next-click":t.nextPage,"prev-click":t.prevPage,"current-change":t.changePage}})],2)},[],!1,null,"7854d2f4",null);e.default=c.exports},3846:function(t,e,o){o("9e1e")&&"g"!=/./g.flags&&o("86cc").f(RegExp.prototype,"flags",{configurable:!0,get:o("0bfb")})},"6b54":function(t,e,o){"use strict";function r(t){o("2aba")(RegExp.prototype,u,t,!0)}o("3846");var n=o("cb7c"),s=o("0bfb"),a=o("9e1e"),u="toString",c=/./[u];o("79e5")(function(){return"/a/b"!=c.call({source:"a",flags:"b"})})?r(function(){var t=n(this);return"/".concat(t.source,"/","flags"in t?t.flags:!a&&t instanceof RegExp?s.call(t):void 0)}):c.name!=u&&r(function(){return c.call(this)})},"7f7f":function(t,e,o){var r=o("86cc").f,n=Function.prototype,s=/^\s*function ([^ (]*)/;"name"in n||o("9e1e")&&r(n,"name",{configurable:!0,get:function(){try{return(""+this).match(s)[1]}catch(t){return""}}})},d9f9:function(t,e,o){}}]);