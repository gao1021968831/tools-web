<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <h2 class="page-title">IP格式转换</h2>
      </template>

      <el-form @submit.prevent="convert" class="page-form">
        <el-form-item class="radio-group-item">
          <el-radio-group v-model="convertType" class="format-radio">
            <el-radio :value="'dec2bin'">十进制转二进制</el-radio>
            <el-radio :value="'bin2dec'">二进制转十进制</el-radio>
            <el-radio :value="'dec2hex'">十进制转十六进制</el-radio>
            <el-radio :value="'hex2dec'">十六进制转十进制</el-radio>
            <el-radio :value="'mask2cidr'">掩码转CIDR</el-radio>
            <el-radio :value="'cidr2mask'">CIDR转掩码</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item class="textarea-item">
          <el-input
            v-model="inputText"
            type="textarea"
            :rows="8"
            :placeholder="inputPlaceholder"
            @keyup.ctrl.enter="convert"
            @keyup.enter="handleEnter">
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
          :rows="8"
          readonly>
        </el-input>
      </div>
    </el-card>
  </div>
</template>

<script>
import { formatIp } from '../api/ip'
import { ElMessage } from 'element-plus'

export default {
  name: 'IpFormat',
  data() {
    return {
      convertType: 'dec2bin',
      inputText: '',
      result: [],
      loading: false
    }
  },
  computed: {
    inputPlaceholder() {
      const placeholders = {
        dec2bin: '请输入十进制IP地址，每行一个（如：192.168.1.1）',
        bin2dec: '请输入二进制IP地址，每行一个（如：11000000.10101000.00000001.00000001）',
        dec2hex: '请输入十进制IP地址，每行一个（如：192.168.1.1）',
        hex2dec: '请输入十六进制IP地址，每行一个（如：C0.A8.01.01）',
        mask2cidr: '请输入子网掩码，每行一个（如：255.255.255.0）',
        cidr2mask: '请输入CIDR格式，每行一个（如：24）'
      }
      return placeholders[this.convertType]
    },
    resultText() {
      return this.result.join('\n')
    }
  },
  watch: {
    convertType() {
      this.clearInput()
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
      if (!this.inputText.trim()) {
        ElMessage.warning('请输入需要转换的内容')
        return
      }

      const inputs = this.inputText.split('\n').filter(ip => ip.trim())
      
      this.loading = true
      try {
        const res = await formatIp({
          type: this.convertType,
          inputs
        })
        this.result = Array.isArray(res) ? res : res.data || []
        ElMessage.success('转换成功')
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
    async copyResult() {
      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(this.resultText)
          ElMessage.success('复制成功')
          return
        }
        
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
    handleEnter(e) {
      e.preventDefault()
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
@import '../assets/styles/common.css';

/* IP格式转换特定样式 */
.format-radio {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

@media screen and (max-width: 768px) {
  .format-radio {
    flex-direction: column;
  }

  .format-radio :deep(.el-radio-button) {
    width: 100%;
  }

  .format-radio :deep(.el-radio-button__inner) {
    width: 100%;
    border-radius: 4px !important;
  }

  .format-radio :deep(.el-radio-button:first-child .el-radio-button__inner) {
    border-radius: 4px !important;
  }

  .format-radio :deep(.el-radio-button:last-child .el-radio-button__inner) {
    border-radius: 4px !important;
  }
}
</style> 