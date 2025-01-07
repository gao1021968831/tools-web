<template>
  <div class="ip-summary">
    <el-card>
      <template #header>
        <h2>IP汇总</h2>
      </template>

      <el-form @submit.prevent="summarize">
        <el-form-item>
          <el-input
            v-model="ipInput"
            type="textarea"
            :rows="8"
            placeholder="请输入IP地址列表，每行一个IP或IP段"
            @keyup.ctrl.enter="summarize">
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="summarize" :loading="loading">汇总</el-button>
          <el-button @click="clearInput">清空输入</el-button>
          <el-button type="success" @click="copyResult" :disabled="!result.length">复制结果</el-button>
        </el-form-item>
      </el-form>

      <div v-if="result.length" class="result">
        <h3>汇总结果:</h3>
        <el-input
          v-model="resultText"
          type="textarea"
          :rows="8"
          readonly
        ></el-input>
      </div>
    </el-card>
  </div>
</template>

<script>
import { summarizeIps } from '../api/ip'
import { ElMessage } from 'element-plus'

export default {
  name: 'IpSummary',
  data() {
    return {
      ipInput: '',
      result: [],
      loading: false
    }
  },
  computed: {
    resultText() {
      return this.result.join('\n')
    }
  },
  mounted() {
    window.addEventListener('keydown', this.handleKeydown)
  },
  unmounted() {
    window.removeEventListener('keydown', this.handleKeydown)
  },
  methods: {
    async summarize() {
      if (!this.ipInput.trim()) {
        ElMessage.warning('请输入IP地址')
        return
      }

      const ipRanges = this.ipInput.split('\n').filter(ip => ip.trim())
      
      this.loading = true
      try {
        const res = await summarizeIps({ ipRanges })
        this.result = res.data
        ElMessage.success('汇总成功')
      } catch (error) {
        // 错误已在请求拦截器中处理
      } finally {
        this.loading = false
      }
    },
    clearInput() {
      this.ipInput = ''
      this.result = []
    },
    copyResult() {
      navigator.clipboard.writeText(this.resultText)
        .then(() => ElMessage.success('复制成功'))
        .catch(() => ElMessage.error('复制失败'))
    },
    handleKeydown(e) {
      if (e.ctrlKey && e.key === 'Enter') {
        this.summarize()
      }
    }
  }
}
</script>

<style scoped>
.ip-summary {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.result {
  margin-top: 20px;
}
</style> 