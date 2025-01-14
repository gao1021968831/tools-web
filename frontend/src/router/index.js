import { createRouter, createWebHistory } from 'vue-router'
import NetworkCalc from '../views/NetworkCalc.vue'
import IpSummary from '../views/IpSummary.vue'
import IpConversion from '../views/IpConversion.vue'
import IpFormat from '../views/IpFormat.vue'
import SubnetCalc from '../views/SubnetCalc.vue'
import IpLocation from '../views/IpLocation.vue'
import DnsQuery from '../views/DnsQuery.vue'

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
  },
  {
    path: '/subnet-calc',
    name: 'SubnetCalc',
    component: SubnetCalc
  },
  {
    path: '/ip-location',
    name: 'IpLocation',
    component: IpLocation
  },
  {
    path: '/dns-query',
    name: 'DnsQuery',
    component: DnsQuery
  },
  {
    path: '/doc-convert',
    name: 'DocConvert',
    component: () => import('../views/DocConvert.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 