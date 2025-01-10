<template>
  <div class="ip-conversion">
    <el-card>
      <template #header>
        <h2 class="page-title">IP转换</h2>
      </template>

      <el-form @submit.prevent="convert" class="conversion-form">
        <el-form-item class="radio-group-item">
          <el-radio-group v-model="direction" class="direction-radio">
            <el-radio :value="'v4tov6'">IPv4 转 IPv6</el-radio>
            <el-radio :value="'v6tov4'">IPv6 转 IPv4</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="direction === 'v4tov6'" class="prefix-input">
          <el-input
            v-model="ipv6Prefix"
            placeholder="请输入IPv6前缀(例如: 2409:8C20:28C1:0400::)"
            @keyup.enter="convert">
          </el-input>
        </el-form-item>

        <el-form-item class="textarea-item">
          <el-input
            v-model="ipInput"
            type="textarea"
            :rows="inputRows"
            :placeholder="inputPlaceholder"
            @keyup.ctrl.enter="convert">
          </el-input>
        </el-form-item>

        <el-form-item class="button-group">
          <el-button type="primary" @click="convert" :loading="loading">转换</el-button>
          <el-button @click="clearInput">清空输入</el-button>
          <el-button type="success" @click="copyResult" :disabled="!result.length">复制结果</el-button>
        </el-form-item>
      </el-form>

      <div v-if="result.length" class="result">
        <h3 class="result-title">转换结果:</h3>
        <el-input
          v-model="resultText"
          type="textarea"
          :rows="outputRows"
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
      loading: false,
      textareaRows: {
        v4tov6: {
          input: 8,
          output: 12
        },
        v6tov4: {
          input: 12,
          output: 8
        }
      }
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
    },
    inputRows() {
      return this.textareaRows[this.direction].input
    },
    outputRows() {
      return this.textareaRows[this.direction].output
    }
  },
  mounted() {
    window.addEventListener('keydown', this.handleKeydown)
  },
  unmounted() {
    window.removeEventListener('keydown', this.handleKeydown)
  },
  watch: {
    direction() {
      this.ipInput = ''
      this.result = []
    }
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
    async copyResult() {
      try {
        // 首先尝试使用现代的 Clipboard API
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(this.resultText)
          ElMessage.success('复制成功')
          return
        }
        
        // 降级方案：使用传统方法
        const textarea = document.createElement('textarea')
        textarea.value = this.resultText
        textarea.style.position = 'fixed'
        textarea.style.opacity = '0'
        document.body.appendChild(textarea)
        
        textarea.select()
        const success = document.execCommand('copy')
        document.body.removeChild(textarea)
        
        if (success) {
          ElMessage.success('复制成功')
        } else {
          throw new Error('复制操作失败')
        }
      } catch (err) {
        console.error('Copy failed:', err)
        ElMessage.error('复制失败')
      }
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
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

.page-title {
  margin: 0;
  font-size: 1.5rem;
  color: var(--el-text-color-primary);
}

.conversion-form {
  width: 100%;
}

.radio-group-item {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.direction-radio {
  width: 100%;
  display: flex;
  justify-content: center;
}

.prefix-input {
  margin-bottom: 20px;
}

.textarea-item :deep(.el-textarea__inner) {
  resize: none;
  font-family: monospace;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.result {
  margin-top: 20px;
}

.result-title {
  margin-bottom: 10px;
  font-size: 1.1rem;
  color: var(--el-text-color-primary);
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .ip-conversion {
    padding: 10px;
  }

  .page-title {
    font-size: 1.2rem;
  }

  .direction-radio {
    flex-direction: column;
    gap: 10px;
  }

  .direction-radio :deep(.el-radio-button) {
    width: 100%;
  }

  .direction-radio :deep(.el-radio-button__inner) {
    width: 100%;
    border-radius: 4px !important;
  }

  .direction-radio :deep(.el-radio-button:first-child .el-radio-button__inner) {
    border-radius: 4px !important;
    margin-bottom: 5px;
  }

  .direction-radio :deep(.el-radio-button:last-child .el-radio-button__inner) {
    border-radius: 4px !important;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group .el-button {
    width: 100%;
  }

  .result-title {
    font-size: 1rem;
  }

  /* 调整输入框在移动端的显示 */
  :deep(.el-textarea__inner) {
    font-size: 14px;
  }

  /* 调整表单项间距 */
  .el-form-item {
    margin-bottom: 15px;
  }
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .page-title,
  .result-title {
    color: var(--el-text-color-primary);
  }
}
</style> 