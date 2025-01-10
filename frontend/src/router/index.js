import { createRouter, createWebHistory } from 'vue-router'
import NetworkCalc from '../views/NetworkCalc.vue'
import IpSummary from '../views/IpSummary.vue'
import IpConversion from '../views/IpConversion.vue'
import IpFormat from '../views/IpFormat.vue'

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
  },
  {
    path: '/ip-format',
    name: 'IpFormat',
    component: IpFormat
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 