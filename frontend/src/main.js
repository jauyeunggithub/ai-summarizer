import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from '@/App.vue'
import router from '@/router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import 'bootstrap-icons/font/bootstrap-icons.css'
import '@/style.css'
import moment from 'moment'

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.mount('#app')

app.config.globalProperties.$formatDate = (date) => {
  return moment(date).format('YYYY-MM-DD HH:mm')
}
