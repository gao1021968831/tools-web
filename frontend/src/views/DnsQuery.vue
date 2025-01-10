<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <h2 class="page-title">DNS查询工具</h2>
      </template>

      <el-form :model="form" @submit.prevent="query" class="page-form">
        <el-form-item label="域名">
          <el-input
            v-model="form.domain"
            placeholder="请输入域名（如：example.com）"
            @keyup.enter="query">
          </el-input>
        </el-form-item>

        <el-form-item label="记录类型">
          <div class="record-type-control">
            <el-button 
              size="small" 
              @click="toggleSelectAll" 
              :type="isAllSelected ? 'primary' : ''"
              class="select-all-btn">
              {{ isAllSelected ? '取消全选' : '全选' }}
            </el-button>
            <el-checkbox-group v-model="form.types">
              <el-checkbox-button :value="'A'">A</el-checkbox-button>
              <el-checkbox-button :value="'AAAA'">AAAA</el-checkbox-button>
              <el-checkbox-button :value="'MX'">MX</el-checkbox-button>
              <el-checkbox-button :value="'NS'">NS</el-checkbox-button>
              <el-checkbox-button :value="'CNAME'">CNAME</el-checkbox-button>
              <el-checkbox-button :value="'TXT'">TXT</el-checkbox-button>
            </el-checkbox-group>
          </div>
        </el-form-item>

        <el-form-item class="button-group">
          <el-button type="primary" @click="query" :loading="loading">查询</el-button>
          <el-button @click="clearForm">清空</el-button>
        </el-form-item>
      </el-form>

      <div v-if="result.length" class="result">
        <h3 class="result-title">查询结果:</h3>
        <el-collapse v-model="activeNames">
          <el-collapse-item 
            v-for="item in result" 
            :key="item.type" 
            :title="getRecordTitle(item)" 
            :name="item.type">
            <el-table 
              :data="item.records" 
              border 
              style="width: 100%"
              :row-class-name="getRowClassName">
              <el-table-column prop="name" label="名称" min-width="120" show-overflow-tooltip />
              <el-table-column prop="type" label="类型" width="100" />
              <el-table-column prop="value" label="值" min-width="200" show-overflow-tooltip />
              <el-table-column prop="ttl" label="TTL" width="100" />
            </el-table>
          </el-collapse-item>
        </el-collapse>
      </div>
    </el-card>
  </div>
</template>

<script>
import { queryDns } from '../api/ip'
import { ElMessage } from 'element-plus'

export default {
  name: 'DnsQuery',
  data() {
    return {
      form: {
        domain: '',
        types: ['A']  // 默认查询A记录
      },
      result: [],
      loading: false,
      activeNames: [],
      allRecordTypes: ['A', 'AAAA', 'MX', 'NS', 'CNAME', 'TXT']  // 所有可选记录类型
    }
  },
  computed: {
    isAllSelected() {
      return this.form.types.length === this.allRecordTypes.length
    }
  },
  methods: {
    async query() {
      if (!this.form.domain) {
        ElMessage.warning('请输入域名')
        return
      }

      if (!this.form.types.length) {
        ElMessage.warning('请选择至少一种记录类型')
        return
      }

      this.loading = true
      try {
        const res = await queryDns(this.form)
        if (res.data && Array.isArray(res.data)) {
          this.result = res.data
          this.activeNames = this.result.map(item => item.type)  // 自动展开所有结果
          ElMessage.success('查询成功')
        } else {
          throw new Error('返回数据格式错误')
        }
      } catch (error) {
        // 错误已在请求拦截器中处理
        this.result = []
      } finally {
        this.loading = false
      }
    },
    toggleSelectAll() {
      if (this.isAllSelected) {
        this.form.types = []
      } else {
        this.form.types = [...this.allRecordTypes]
      }
    },
    clearForm() {
      this.form.domain = ''
      this.form.types = ['A']
      this.result = []
      this.activeNames = []
    },
    getRecordTitle(item) {
      const count = item.records.length
      const hasError = item.records.some(record => record.value.includes('查询失败') || record.value.includes('查询错误'))
      return `${item.type} 记录 ${hasError ? '(查询失败)' : `(${count}条)`}`
    },
    getRowClassName({ row }) {
      if (row.value.includes('查询失败') || row.value.includes('查询错误')) {
        return 'error-row'
      }
      return ''
    }
  }
}
</script>

<style scoped>
@import '../assets/styles/common.css';

.record-type-control {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.select-all-btn {
  flex-shrink: 0;
}

.el-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.result {
  margin-top: 20px;
}

:deep(.error-row) {
  color: var(--el-color-danger);
}

:deep(.el-collapse-item__header) {
  font-size: 16px;
  font-weight: bold;
}

:deep(.el-table .cell) {
  word-break: break-all;
}

@media screen and (max-width: 768px) {
  .record-type-control {
    flex-direction: column;
  }

  .select-all-btn {
    width: 100%;
    margin-bottom: 10px;
  }

  .el-checkbox-group {
    flex-direction: column;
  }

  :deep(.el-checkbox-button) {
    width: 100%;
  }

  :deep(.el-checkbox-button__inner) {
    width: 100%;
  }

  :deep(.el-table) {
    font-size: 12px;
  }
}
</style> 