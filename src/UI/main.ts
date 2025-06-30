import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './styles/global.css'

import HomePage from './pages/HomePage.vue'
import TrainPage from './pages/TrainPage.vue'
import InferPage from './pages/InferPage.vue'
import TunePage from './pages/TunePage.vue'
import ModelPage from './pages/ModelPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomePage },
    { path: '/train', name: 'train', component: TrainPage },
    { path: '/infer', name: 'infer', component: InferPage },
    { path: '/tune', name: 'tune', component: TunePage },
    { path: '/model', name: 'model', component: ModelPage },
  ]
})

const app = createApp(App)
app.use(router)
app.mount('#app') 