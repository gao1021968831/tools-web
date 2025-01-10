<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <h2 class="page-title">子网划分</h2>
      </template>

      <el-form :model="form" @submit.prevent="calculate" class="page-form">
        <el-form-item label="主网段">
          <el-input 
            v-model="form.network"
            placeholder="请输入主网段（如：192.168.0.0/24）"
            @keyup.enter="calculate">
          </el-input>
        </el-form-item>

        <el-form-item label="划分方式">
          <el-radio-group v-model="form.divideType">
            <el-radio-button label="count">按子网数量</el-radio-button>
            <el-radio-button label="hosts">按主机数量</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item :label="form.divideType === 'count' ? '子网数量' : '每个子网主机数'">
          <el-input-number 
            v-model="form.value"
            :min="1"
            :max="form.divideType === 'count' ? 256 : 65534"
            @keyup.enter="calculate">
          </el-input-number>
        </el-form-item>

        <el-form-item class="button-group">
          <el-button type="primary" @click="calculate" :loading="loading">计算</el-button>
          <el-button @click="clearForm">清空</el-button>
        </el-form-item>
      </el-form>

      <div v-if="result.length" class="result">
        <h3 class="result-title">划分结果:</h3>
        <el-table :data="result" border style="width: 100%">
          <el-table-column prop="subnet" label="子网" />
          <el-table-column prop="netmask" label="子网掩码" />
          <el-table-column prop="hosts" label="可用主机数" />
          <el-table-column prop="range" label="可用地址范围" />
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
        network: '',
        divideType: 'count',
        value: 2
      },
      result: [],
      loading: false
    }
  },
  methods: {
    async calculate() {
      if (!this.form.network) {
        ElMessage.warning('请输入主网段')
        return
      }

      this.loading = true
      try {
        const res = await divideSubnet(this.form)
        this.result = res.data
        ElMessage.success('计算成功')
      } catch (error) {
        // 错误已在请求拦截器中处理
      } finally {
        this.loading = false
      }
    },
    clearForm() {
      this.form.network = ''
      this.form.value = 2
      this.result = []
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
</style> 