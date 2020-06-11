// npm i -D compression-webpack-plugin
const CompressionPlugin = require('compression-webpack-plugin')
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')

function getProdExternals() {
  return {
    // axios: "axios",
    // "chart.js": "Chart",
    'vue': "Vue",
    'vue-router': "VueRouter",
    'vuex': "Vuex",
    'axios': 'axios',
    'echarts': 'echarts',
    'v-charts': 'VCharts',
    'element-ui': 'ElementUI'
  };
}

module.exports = {
    // 基本路径 baseURL已经过时
    publicPath: '/',  
    // 输出文件目录
    outputDir: 'dist',
    // eslint-loader 是否在保存的时候检查
    lintOnSave: true,
    // use the full build with in-browser compiler?
    // https://vuejs.org/v2/guide/installation.html#Runtime-Compiler-vs-Runtime-only
    // compiler: false,
    // webpack配置
    // see https://github.com/vuejs/vue-cli/blob/dev/docs/webpack.md
    chainWebpack: (config) => {
      // 移除 prefetch 插件
      config.plugins.delete('prefetch')
    },
    // configureWebpack: () => {},
    configureWebpack: config => {
        if (process.env.NODE_ENV === 'production') {
          return {
            externals: getProdExternals(),
            plugins: [
              new BundleAnalyzerPlugin(),  // 使用默认配置
              new UglifyJsPlugin({
                uglifyOptions: {
                  compress: {
                    drop_debugger: true,
                    drop_console: true,
                  },
                },
                sourceMap: false,
                parallel: true,
              }),
              new CompressionPlugin({
                algorithm: 'gzip',
                test: /\.(js|css)$/,// 匹配文件名
                threshold: 10240, // 对超过10k的数据压缩
                deleteOriginalAssets: false, // 不删除源文件
                minRatio: 0.8 // 压缩比
              })
            ]
          }
        }
      },
    // vue-loader 配置项
    // https://vue-loader.vuejs.org/en/options.html
    // vueLoader: {},
    // 生产环境是否生成 sourceMap 文件, false for pro
    productionSourceMap: false,
    // css相关配置
    css: {
     // 是否使用css分离插件 ExtractTextPlugin
     extract: true,
     // 开启 CSS source maps?
     sourceMap: false,
     // css预设器配置项
     loaderOptions: {},
     // 启用 CSS modules for all css / pre-processor files.
     modules: false
    },
    // use thread-loader for babel & TS in production build
    // enabled by default if the machine has more than 1 cores
    parallel: require('os').cpus().length > 1,
    // 是否启用dll
    // See https://github.com/vuejs/vue-cli/blob/dev/docs/cli-service.md#dll-mode
    // dll: false,
    // PWA 插件相关配置
    // see https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-pwa
    pwa: {},
    // webpack-dev-server 相关配置
    // devServer: {
    //   open: process.platform === 'darwin',
    //   disableHostCheck: true,
    //   host: 'www.test.com',//如果是真机测试，就使用这个IP
    //   port: 1234,
    //   https: false,
    //   hotOnly: false,
    //  before: app => {}
    // },
    // 第三方插件配置
    pluginOptions: {
     // ...
    }
   }