<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <h2 class="page-title">IP归属地查询</h2>
      </template>

      <!-- 当前IP信息展示 -->
      <div v-if="currentLocation" class="current-ip-info">
        <h3>您的IP信息：</h3>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="IP地址">{{ currentLocation.ip }}</el-descriptions-item>
          <el-descriptions-item label="国家/地区">{{ currentLocation.country }}</el-descriptions-item>
          <el-descriptions-item label="省份">{{ currentLocation.region }}</el-descriptions-item>
          <el-descriptions-item label="城市">{{ currentLocation.city }}</el-descriptions-item>
          <el-descriptions-item label="运营商">{{ currentLocation.isp }}</el-descriptions-item>
        </el-descriptions>
      </div>

      <el-divider>批量查询</el-divider>

      <el-form :model="form" @submit.prevent="query" class="page-form">
        <el-form-item label="IP地址">
          <el-input
            v-model="form.ips"
            type="textarea"
            :rows="5"
            placeholder="请输入要查询的IP地址，每行一个"
            @keyup.ctrl.enter="query">
          </el-input>
        </el-form-item>

        <el-form-item class="button-group">
          <el-button type="primary" @click="query" :loading="loading">查询</el-button>
          <el-button @click="clearForm">清空</el-button>
        </el-form-item>
      </el-form>

      <!-- 查询结果表格 -->
      <div v-if="result.length" class="result">
        <h3 class="result-title">查询结果:</h3>
        <el-table :data="result" border style="width: 100%">
          <el-table-column prop="ip" label="IP地址" min-width="140" />
          <el-table-column prop="country" label="国家/地区" min-width="120" />
          <el-table-column prop="region" label="省份" min-width="120" />
          <el-table-column prop="city" label="城市" min-width="120" />
          <el-table-column prop="isp" label="运营商" min-width="140" />
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import { queryIpLocation, getCurrentIpLocation } from '../api/ip'
import { ElMessage } from 'element-plus'

export default {
  name: 'IpLocation',
  data() {
    return {
      form: {
        ips: ''
      },
      result: [],
      loading: false,
      currentLocation: null
    }
  },
  created() {
    // 页面创建时获取当前IP信息
    this.getCurrentLocation()
  },
  methods: {
    async getCurrentLocation() {
      try {
        const res = await getCurrentIpLocation()
        this.currentLocation = res.data
      } catch (error) {
        ElMessage.error('获取当前IP信息失败')
      }
    },
    async query() {
      if (!this.form.ips.trim()) {
        ElMessage.warning('请输入要查询的IP地址')
        return
      }

      const ips = this.form.ips.split('\n')
        .map(ip => ip.trim())
        .filter(ip => ip)

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
    clearForm() {
      this.form.ips = ''
      this.result = []
    }
  }
}
</script>

<style scoped>
@import '../assets/styles/common.css';

.current-ip-info {
  margin-bottom: 20px;
}

.current-ip-info h3 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
}

.el-divider {
  margin: 24px 0;
}

:deep(.el-descriptions) {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

:deep(.el-descriptions__label) {
  width: 100px;
  color: #606266;
}

:deep(.el-descriptions__content) {
  color: #303133;
}

@media screen and (max-width: 768px) {
  .current-ip-info {
    margin-bottom: 15px;
  }

  :deep(.el-descriptions__label) {
    width: 80px;
  }
}
</style> 