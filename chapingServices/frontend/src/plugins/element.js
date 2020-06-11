import Vue from 'vue'
// import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

// Vue.use(Element)

// 只加载使用使用的组件
import {Button, Input, 
    Pagination, Table, TableColumn,
    Form, Badge, FormItem,
    Progress, Header, Main,
    Step, Steps,Message,
    Row, Col
} from 'element-ui'

Vue.use(Button)
Vue.use(Input)
Vue.use(Pagination)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Badge)
Vue.use(Progress)
Vue.use(Header)
Vue.use(Main)
Vue.use(Step)
Vue.use(Steps)
Vue.use(Row)
Vue.use(Col)

Vue.prototype.$message = Message