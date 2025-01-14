<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <h2 class="page-title">文档转换</h2>
      </template>

      <el-form class="upload-form">
        <el-form-item>
          <el-upload
            class="upload-area"
            drag
            action="#"
            :headers="headers"
            :before-upload="handleFileSelect"
            :auto-upload="false"
            :limit="1"
            :file-list="fileList"
            :disabled="converting"
            :on-change="handleFileChange"
            :on-remove="handleRemove">
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 PDF 转 Word 或 Word 转 PDF（文件大小不超过10MB）
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item v-show="fileList.length > 0" class="action-buttons">
          <el-button 
            type="primary" 
            @click="handleConvert" 
            :loading="converting"
            :disabled="converting">
            {{ converting ? '转换中...' : '开始转换' }}
          </el-button>
          <el-button 
            type="success" 
            v-if="convertedFile"
            @click="handleDownload">
            下载 {{ convertedFileName }}
          </el-button>
          <el-button 
            type="warning" 
            @click="handleReset"
            :disabled="converting">
            重新选择
          </el-button>
        </el-form-item>

        <div v-if="convertedFile" class="conversion-info">
          <p>原始文件：{{ originalFileName }}</p>
          <p>转换后文件：{{ convertedFileName }}</p>
        </div>
      </el-form>

      <div v-if="converting" class="converting-status">
        <el-progress type="circle" :percentage="progress"></el-progress>
        <p>正在转换中，请稍候...</p>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { baseURL } from '../config'
import axios from 'axios'

export default {
  name: 'DocConvert',
  components: {
    UploadFilled
  },
  setup() {
    const converting = ref(false)
    const progress = ref(0)
    const fileList = ref([])
    const selectedFile = ref(null)
    const convertedFile = ref(null)
    const originalFileName = ref('')
    const convertedFileName = ref('')

    const headers = {
      'X-Requested-With': 'XMLHttpRequest'
    }

    // 添加文件改变事件处理
    const handleFileChange = (file) => {
      console.log('File changed:', file)
      if (file) {
        fileList.value = [file.raw]
        selectedFile.value = file.raw
        originalFileName.value = file.raw.name
        convertedFileName.value = ''
        convertedFile.value = null
      }
    }

    // 修改文件选择处理
    const handleFileSelect = (file) => {
      // 获取原始文件名和扩展名
      let originalName = file.name
      let fileExt = originalName.substring(originalName.lastIndexOf('.')).toLowerCase()
      
      // 验证文件类型
      const isPDF = (fileExt === '.pdf' && 
                    (file.type === 'application/pdf' || 
                     file.type === 'application/octet-stream'))
      
      const isDOCX = (fileExt === '.docx' && 
                     (file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
                      file.type === 'application/msword' ||
                      file.type === 'application/octet-stream'))
      
      const isValidType = isPDF || isDOCX
      const isLt10M = file.size / 1024 / 1024 < 10

      if (!isValidType) {
        ElMessage.error(`不支持的文件类型: ${file.type}，仅支持PDF和DOCX文件！`)
        return false
      }
      if (!isLt10M) {
        ElMessage.error('文件大小不能超过10MB！')
        return false
      }

      console.log('File selected:', file.name)
      return true  // 允许选择文件
    }

    // 添加文件移除处理
    const handleRemove = () => {
      selectedFile.value = null
      fileList.value = []
      convertedFile.value = null
      progress.value = 0
    }

    // 转换处理
    const handleConvert = async () => {
      if (!selectedFile.value) {
        ElMessage.warning('请先选择文件')
        return
      }

      converting.value = true
      progress.value = 0
      
      const formData = new FormData()
      formData.append('file', selectedFile.value)
      
      try {
        const response = await axios.post('/api/doc/convert', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            ...headers
          },
          responseType: 'blob'
        })
        
        // 从响应头获取文件名
        const contentDisposition = response.headers['content-disposition']
        let filename = ''
        if (contentDisposition) {
          // 优先使用 filename* 字段
          const filenameStarMatch = contentDisposition.match(/filename\*=UTF-8''([^;]*)/i)
          if (filenameStarMatch) {
            filename = decodeURIComponent(filenameStarMatch[1])
          } else {
            // 回退到普通 filename
            const filenameMatch = contentDisposition.match(/filename="([^"]*)"/)
            if (filenameMatch) {
              filename = decodeURIComponent(filenameMatch[1])
            }
          }
        }
        
        // 如果没有从响应头获取到文件名，则根据原文件名生成
        if (!filename) {
          const originalName = selectedFile.value.name
          const isSourcePDF = originalName.toLowerCase().endsWith('.pdf')
          const baseName = originalName.substring(0, originalName.lastIndexOf('.'))
          filename = `${baseName}${isSourcePDF ? '.docx' : '.pdf'}`
        }

        // 确保文件名不为空
        if (!filename) {
          filename = `converted${selectedFile.value.name.toLowerCase().endsWith('.pdf') ? '.docx' : '.pdf'}`
        }

        convertedFileName.value = filename
        convertedFile.value = {
          blob: new Blob([response.data], {
            type: selectedFile.value.name.toLowerCase().endsWith('.pdf') ? 
              'application/vnd.openxmlformats-officedocument.wordprocessingml.document' : 
              'application/pdf'
          }),
          filename: filename
        }
        
        converting.value = false
        progress.value = 100
        ElMessage.success('转换成功！')
      } catch (error) {
        handleError(error)
      }
    }

    // 下载处理
    const handleDownload = () => {
      if (!convertedFile.value) {
        ElMessage.warning('没有可下载的文件')
        return
      }

      const { blob, filename } = convertedFile.value
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    }

    // 重置处理
    const handleReset = () => {
      handleRemove()
    }

    const handleError = (error) => {
      converting.value = false
      progress.value = 0
      
      let errorMessage = '未知错误'
      if (error.response && error.response.data && error.response.data.error) {
        errorMessage = error.response.data.error
      } else if (error.message) {
        errorMessage = error.message
      }
      
      ElMessage.error('转换失败：' + errorMessage)
      console.error('File conversion error:', error)
    }

    return {
      converting,
      progress,
      fileList,
      selectedFile,
      convertedFile,
      originalFileName,
      convertedFileName,
      handleFileSelect,
      handleFileChange,
      handleConvert,
      handleDownload,
      handleReset,
      handleError,
      handleRemove,
      headers
    }
  }
}
</script>

<style scoped>
.upload-form {
  max-width: 600px;
  margin: 0 auto;
}

.upload-area {
  width: 100%;
}

.converting-status {
  text-align: center;
  margin-top: 20px;
}

.action-buttons {
  display: block !important;
  margin-top: 20px;
  text-align: center;
}

.action-buttons .el-button {
  margin: 0 10px;
}

:deep(.el-upload-dragger) {
  width: 100%;
}

:deep(.el-upload__tip) {
  margin-top: 10px;
  color: #909399;
}

@media screen and (max-width: 768px) {
  .action-buttons .el-button {
    margin: 5px;
  }
}

.conversion-info {
  margin-top: 20px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.conversion-info p {
  margin: 5px 0;
  color: #606266;
}
</style> 