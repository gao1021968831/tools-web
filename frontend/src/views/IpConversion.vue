<template>
  <div class="ip-conversion">
    <el-card>
      <template #header>
        <h2>IP转换</h2>
      </template>

      <el-form @submit.prevent="convert">
        <el-form-item>
          <el-radio-group v-model="direction">
            <el-radio-button label="v4tov6">IPv4转IPv6</el-radio-button>
            <el-radio-button label="v6tov4">IPv6转IPv4</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="direction === 'v4tov6'">
          <el-input
            v-model="ipv6Prefix"
            placeholder="请输入IPv6前缀(例如: 2409:8C20:28C1:0400::)"
            @keyup.enter="convert">
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-input
            v-model="ipInput"
            type="textarea"
            :rows="8"
            :placeholder="inputPlaceholder"
            @keyup.ctrl.enter="convert">
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="convert" :loading="loading">转换</el-button>
          <el-button @click="clearInput">清空输入</el-button>
          <el-button type="success" @click="copyResult" :disabled="!result.length">复制结果</el-button>
        </el-form-item>
      </el-form>

      <div v-if="result.length" class="result">
        <h3>转换结果:</h3>
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
import { convertIp } from '../api/ip'
import { ElMessage } from 'element-plus'

export default {
  name: 'IpConversion',
  data() {
    return {
      direction: 'v4tov6',
      ipv6Prefix: '2409:8C20:28C1:0400::',
      ipInput: '',
      result: [],
      loading: false
    }
  },
  computed: {
    inputPlaceholder() {
      return this.direction === 'v4tov6' 
        ? '请输入IPv4地址列表，每行一个' 
        : '请输入IPv6地址列表，每行一个'
    },
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
    async convert() {
      if (!this.ipInput.trim()) {
        ElMessage.warning('请输入IP地址')
        return
      }

      if (this.direction === 'v4tov6' && !this.ipv6Prefix) {
        ElMessage.warning('请输入IPv6前缀')
        return
      }

      const ips = this.ipInput.split('\n').filter(ip => ip.trim())
      
      this.loading = true
      try {
        const res = await convertIp({
          direction: this.direction,
          ips,
          ipv6Prefix: this.ipv6Prefix
        })
        this.result = res.data
        ElMessage.success('转换成功')
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
        this.convert()
      }
    }
  }
}
</script>

<style scoped>
.ip-conversion {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.result {
  margin-top: 20px;
}
</style> 