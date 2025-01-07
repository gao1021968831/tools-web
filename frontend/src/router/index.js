import { createRouter, createWebHashHistory } from 'vue-router'
import NetworkCalc from '../views/NetworkCalc.vue'
import IpSummary from '../views/IpSummary.vue'
import IpConversion from '../views/IpConversion.vue'

const routes = [
  {
    path: '/',
    redirect: '/network-calc'
  },
  {
    path: '/network-calc',
    name: 'NetworkCalc',
    component: NetworkCalc
  },
  {
    path: '/ip-summary',
    name: 'IpSummary',
    component: IpSummary
  },
  {
    path: '/ip-conversion',
    name: 'IpConversion',
    component: IpConversion
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router 