<template>
  <div class="network-calc">
    <el-card>
      <template #header>
        <h2>网段计算</h2>
      </template>

      <el-form :model="form" @submit.prevent="calculate" label-width="120px">
        <el-form-item label="IP地址">
          <el-input 
            v-model="form.ip" 
            placeholder="请输入IP地址"
            @keyup.enter="calculate">
          </el-input>
        </el-form-item>
        
        <el-form-item label="掩码">
          <el-input 
            v-model="form.mask" 
            placeholder="请输入掩码"
            @keyup.enter="calculate">
          </el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="calculate" :loading="loading">计算</el-button>
          <el-button @click="clearForm">清空</el-button>
        </el-form-item>
      </el-form>

      <div v-if="result" class="result">
        <el-descriptions title="计算结果" :column="1" border>
          <el-descriptions-item label="是否是私有地址">{{ result.is_private ? '是' : '否' }}</el-descriptions-item>
          <el-descriptions-item label="所属IP子网">{{ result.network }}</el-descriptions-item>
          <el-descriptions-item label="网络号">{{ result.network_address }}</el-descriptions-item>
          <el-descriptions-item label="广播地址">{{ result.broadcast_address }}</el-descriptions-item>
          <el-descriptions-item label="IP地址总数">{{ result.total_ips }}</el-descriptions-item>
          <el-descriptions-item label="可用IP地址总数">{{ result.usable_ips }}</el-descriptions-item>
          <el-descriptions-item label="起始可用IP地址">{{ result.first_usable }}</el-descriptions-item>
          <el-descriptions-item label="最后可用IP地址">{{ result.last_usable }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script>
import { calculateNetwork } from '../api/ip'
import { ElMessage } from 'element-plus'

export default {
  name: 'NetworkCalc',
  data() {
    return {
      form: {
        ip: '',
        mask: ''
      },
      result: null,
      loading: false
    }
  },
  methods: {
    async calculate() {
      if (!this.form.ip || !this.form.mask) {
        ElMessage.warning('请输入IP地址和掩码')
        return
      }

      this.loading = true
      try {
        const res = await calculateNetwork(this.form)
        this.result = res.data
        ElMessage.success('计算成功')
      } catch (error) {
        // 错误已在请求拦截器中处理
      } finally {
        this.loading = false
      }
    },
    clearForm() {
      this.form.ip = ''
      this.form.mask = ''
      this.result = null
    }
  }
}
</script>

<style scoped>
.network-calc {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.result {
  margin-top: 20px;
}
</style> 