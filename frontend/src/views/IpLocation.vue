<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <h2 class="page-title">IP归属地查询</h2>
      </template>

      <el-form @submit.prevent="query" class="page-form">
        <el-form-item class="textarea-item">
          <el-input
            v-model="inputText"
            type="textarea"
            :rows="8"
            placeholder="请输入IP地址，每行一个（支持IPv4和IPv6）"
            @keyup.ctrl.enter="query"
            @keyup.enter="handleEnter">
          </el-input>
        </el-form-item>

        <el-form-item class="button-group">
          <el-button type="primary" @click="query" :loading="loading">查询</el-button>
          <el-button @click="clearInput">清空输入</el-button>
        </el-form-item>
      </el-form>

      <div v-if="result.length" class="result">
        <h3 class="result-title">查询结果:</h3>
        <el-table :data="result" border style="width: 100%">
          <el-table-column prop="ip" label="IP地址" width="180" />
          <el-table-column prop="country" label="国家/地区" />
          <el-table-column prop="region" label="省份" />
          <el-table-column prop="city" label="城市" />
          <el-table-column prop="isp" label="运营商" />
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import { queryIpLocation } from '../api/ip'
import { ElMessage } from 'element-plus'

export default {
  name: 'IpLocation',
  data() {
    return {
      inputText: '',
      result: [],
      loading: false
    }
  },
  methods: {
    async query() {
      if (!this.inputText.trim()) {
        ElMessage.warning('请输入需要查询的IP地址')
        return
      }

      const ips = this.inputText.split('\n').filter(ip => ip.trim())
      
      this.loading = true
      try {
        const res = await queryIpLocation({ ips })
        this.result = res.data
        ElMessage.success('查询成功')
      } catch (error) {
        // 错误已在请求拦截器中处理
      } finally {
        this.loading = false
      }
    },
    clearInput() {
      this.inputText = ''
      this.result = []
    },
    handleEnter(e) {
      e.preventDefault()
    }
  }
}
</script>

<style scoped>
@import '../assets/styles/common.css';

@media screen and (max-width: 768px) {
  :deep(.el-table) {
    font-size: 12px;
  }
}
</style> 