import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import '@/style.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

console.log('test')

createApp(App).use(router).mount('#app')
