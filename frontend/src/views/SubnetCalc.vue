<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <h2 class="page-title">子网划分</h2>
      </template>

      <el-form :model="form" @submit.prevent="calculate" class="page-form">
        <el-form-item label="主网段">
          <div class="network-input">
            <el-input 
              v-model="form.ip"
              placeholder="请输入网段（如：192.168.0.0）"
              @keyup.enter="calculate">
            </el-input>
            <span class="separator">/</span>
            <el-input
              v-model.number="form.maskBits"
              type="number"
              :min="0"
              :max="32"
              placeholder="掩码位数"
              style="width: 80px"
              @keyup.enter="calculate"
              @input="validateMaskBits">
            </el-input>
          </div>
        </el-form-item>

        <el-form-item label="划分方式">
          <el-radio-group v-model="form.divideType">
            <el-radio :value="'count'">按子网数量</el-radio>
            <el-radio :value="'hosts'">按主机数量</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item :label="form.divideType === 'count' ? '子网数量' : '每个子网主机数'">
          <el-input-number 
            v-model="form.value"
            :min="1"
            :max="form.divideType === 'count' ? 256 : 65534"
            @keyup.enter="calculate">
          </el-input-number>
          <div class="help-text" v-if="form.divideType === 'hosts'">
            注意：每个子网会预留两个地址：
            <ul>
              <li>1个网络地址（Network Address）</li>
              <li>1个广播地址（Broadcast Address）</li>
            </ul>
            例如：需要30个主机时，会分配/27子网（32个地址，减去2个预留地址后正好30个可用地址）
          </div>
        </el-form-item>

        <el-form-item class="button-group">
          <el-button type="primary" @click="calculate" :loading="loading">计算</el-button>
          <el-button @click="clearForm">清空</el-button>
        </el-form-item>
      </el-form>

      <div v-if="result.length" class="result">
        <h3 class="result-title">划分结果:</h3>
        <el-table :data="result" border style="width: 100%">
          <el-table-column prop="subnet" label="子网" min-width="140" />
          <el-table-column prop="netmask" label="子网掩码" min-width="140" />
          <el-table-column prop="network" label="网络地址" min-width="140" />
          <el-table-column prop="broadcast" label="广播地址" min-width="140" />
          <el-table-column prop="hosts" label="可用主机数" width="100" />
          <el-table-column prop="range" label="可用地址范围" min-width="240" show-overflow-tooltip />
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import { divideSubnet } from '../api/ip'
import { ElMessage } from 'element-plus'

export default {
  name: 'SubnetCalc',
  data() {
    return {
      form: {
        ip: '',
        maskBits: 24,  // 默认掩码位数为24
        divideType: 'count',
        value: 2
      },
      result: [],
      loading: false
    }
  },
  methods: {
    async calculate() {
      if (!this.form.ip) {
        ElMessage.warning('请输入网段')
        return
      }

      if (this.form.maskBits === null || this.form.maskBits === undefined) {
        ElMessage.warning('请输入掩码位数')
        return
      }

      this.loading = true
      try {
        const network = `${this.form.ip}/${this.form.maskBits}`
        const res = await divideSubnet({
          network,
          divideType: this.form.divideType,
          value: this.form.value
        })
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
      this.form.maskBits = 24
      this.form.value = 2
      this.result = []
    },
    validateMaskBits(value) {
      const num = parseInt(value)
      if (isNaN(num) || num < 0) {
        this.form.maskBits = 0
      } else if (num > 32) {
        this.form.maskBits = 32
      }
    }
  }
}
</script>

<style scoped>
@import '../assets/styles/common.css';

/* 子网划分特定样式 */
.el-radio-group {
  width: 100%;
  display: flex;
  gap: 10px;
}

@media screen and (max-width: 768px) {
  .el-radio-group {
    flex-direction: column;
  }

  :deep(.el-radio-button) {
    width: 100%;
  }

  :deep(.el-radio-button__inner) {
    width: 100%;
    border-radius: 4px !important;
  }

  :deep(.el-form-item__label) {
    width: 120px !important;
  }

  :deep(.el-table) {
    font-size: 12px;
  }
}

:deep(.el-table) {
  font-size: 14px;
}

@media screen and (max-width: 768px) {
  :deep(.el-table) {
    font-size: 12px;
  }
  
  :deep(.el-table .cell) {
    padding: 8px 4px;
  }
}

.help-text {
  font-size: 12px;
  color: #666;
  margin-top: 8px;
  line-height: 1.4;
}

.help-text ul {
  margin: 4px 0 0 20px;
  padding: 0;
}

.help-text li {
  margin-bottom: 4px;
}

.network-input {
  display: flex;
  align-items: center;
  gap: 8px;
}

.separator {
  font-size: 18px;
  color: #606266;
}

@media screen and (max-width: 768px) {
  .network-input {
    flex-direction: row;
    gap: 4px;
  }
}

/* 添加新样式 */
:deep(.el-input-number.is-without-controls .el-input__wrapper) {
  padding: 1px 11px;
}

/* 去掉number类型输入框的上下箭头 */
:deep(input[type="number"]::-webkit-outer-spin-button),
:deep(input[type="number"]::-webkit-inner-spin-button) {
  -webkit-appearance: none;
  margin: 0;
}

:deep(input[type="number"]) {
  -moz-appearance: textfield;
}
</style> 