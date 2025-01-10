<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="header-content">
        <div class="logo">IP工具集</div>
        <el-menu 
          mode="horizontal" 
          router 
          :default-active="$route.path"
          class="nav-menu"
          background-color="transparent"
          text-color="#fff"
          active-text-color="#409EFF">
          <el-menu-item index="/network-calc">
            <el-icon><Monitor /></el-icon>
            网段计算
          </el-menu-item>
          <el-menu-item index="/ip-summary">
            <el-icon><Collection /></el-icon>
            IP汇总
          </el-menu-item>
          <el-menu-item index="/ip-conversion">
            <el-icon><Switch /></el-icon>
            IP转换
          </el-menu-item>
          <el-menu-item index="/ip-format">
            <el-icon><Operation /></el-icon>
            IP格式转换
          </el-menu-item>
          <el-menu-item index="/subnet-calc">
            <el-icon><Operation /></el-icon>
            子网划分
          </el-menu-item>
          <el-menu-item index="/ip-location">
            <el-icon><Location /></el-icon>
            IP归属地
          </el-menu-item>
          <el-menu-item index="/dns-query">
            <el-icon><Connection /></el-icon>
            DNS查询
          </el-menu-item>
        </el-menu>
        <el-button 
          class="about-btn" 
          type="primary"
          link
          @click="showAbout">
          <el-icon><InfoFilled /></el-icon>
          关于
        </el-button>
      </div>
    </el-header>
    
    <el-main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <el-footer class="mobile-footer" height="50px">
      <div class="mobile-nav">
        <router-link to="/network-calc" class="nav-item" custom v-slot="{ navigate, isActive }">
          <div class="nav-item" :class="{ active: isActive }" @click="navigate">
            <el-icon><Monitor /></el-icon>
            <span>网段计算</span>
          </div>
        </router-link>
        
        <router-link to="/ip-summary" class="nav-item" custom v-slot="{ navigate, isActive }">
          <div class="nav-item" :class="{ active: isActive }" @click="navigate">
            <el-icon><Collection /></el-icon>
            <span>IP汇总</span>
          </div>
        </router-link>
        
        <router-link to="/ip-conversion" class="nav-item" custom v-slot="{ navigate, isActive }">
          <div class="nav-item" :class="{ active: isActive }" @click="navigate">
            <el-icon><Switch /></el-icon>
            <span>IP转换</span>
          </div>
        </router-link>
        
        <router-link to="/ip-format" class="nav-item" custom v-slot="{ navigate, isActive }">
          <div class="nav-item" :class="{ active: isActive }" @click="navigate">
            <el-icon><Operation /></el-icon>
            <span>格式转换</span>
          </div>
        </router-link>
        
        <router-link to="/subnet-calc" class="nav-item" custom v-slot="{ navigate, isActive }">
          <div class="nav-item" :class="{ active: isActive }" @click="navigate">
            <el-icon><Operation /></el-icon>
            <span>子网划分</span>
          </div>
        </router-link>
        
        <router-link to="/ip-location" class="nav-item" custom v-slot="{ navigate, isActive }">
          <div class="nav-item" :class="{ active: isActive }" @click="navigate">
            <el-icon><Location /></el-icon>
            <span>归属地</span>
          </div>
        </router-link>
        
        <router-link to="/dns-query" class="nav-item" custom v-slot="{ navigate, isActive }">
          <div class="nav-item" :class="{ active: isActive }" @click="navigate">
            <el-icon><Connection /></el-icon>
            <span>DNS查询</span>
          </div>
        </router-link>
        
        <div class="nav-item" @click="showAbout">
          <el-icon><InfoFilled /></el-icon>
          <span>关于</span>
        </div>
      </div>
    </el-footer>

    <el-dialog
      v-model="showAboutDialog"
      title="关于"
      width="500px"
      class="about-dialog">
      <div class="about-content">
        <h3>IP工具集 <span class="version">v1.3.0</span></h3>
        <p class="desc">一个功能强大的IP地址工具集合，提供多种IP地址相关的计算和转换功能。</p>
        
        <h4>功能列表：</h4>
        <div class="feature-list">
          <div class="feature-item">
            <el-icon><Monitor /></el-icon>
            网段计算
          </div>
          <div class="feature-item">
            <el-icon><Collection /></el-icon>
            IP汇总
          </div>
          <div class="feature-item">
            <el-icon><Switch /></el-icon>
            IP转换
          </div>
          <div class="feature-item">
            <el-icon><Operation /></el-icon>
            格式转换
          </div>
          <div class="feature-item">
            <el-icon><Operation /></el-icon>
            子网划分
          </div>
          <div class="feature-item">
            <el-icon><Location /></el-icon>
            IP归属地
          </div>
          <div class="feature-item">
            <el-icon><Connection /></el-icon>
            DNS查询
          </div>
        </div>

        <h4>更新记录：</h4>
        <div class="update-list">
          <div class="update-item">
            <div class="version-tag">v1.3.0</div>
            <ul>
              <li>✨ 新增IP归属地查询功能</li>
              <li>✨ 新增DNS记录查询功能</li>
              <li>🎨 优化子网划分界面</li>
              <li>🐛 修复子网计算问题</li>
            </ul>
          </div>
          <div class="update-item">
            <div class="version-tag">v1.2.0</div>
            <ul>
              <li>✨ 新增子网划分功能</li>
              <li>🎨 优化表格显示</li>
              <li>⚡️ 改进计算性能</li>
              <li>📱 完善移动端适配</li>
            </ul>
          </div>
          <div class="update-item">
            <div class="version-tag">v1.1.0</div>
            <ul>
              <li>✨ 新增IP格式转换功能</li>
              <li>🎨 优化移动端适配</li>
              <li>🐛 修复已知问题</li>
              <li>⚡️ 性能优化</li>
            </ul>
          </div>
          <div class="update-item">
            <div class="version-tag">v1.0.0</div>
            <ul>
              <li>🎉 首次发布</li>
              <li>✨ 实现网段计算功能</li>
              <li>✨ 实现IP汇总功能</li>
              <li>✨ 实现IPv4/IPv6转换功能</li>
            </ul>
          </div>
        </div>

        <div class="footer">
          <p>作者：gcg</p>
          <p>
            <a href="https://github.com/gcg88/ip-tools" target="_blank">
              GitHub 仓库
            </a>
          </p>
        </div>
      </div>
    </el-dialog>
  </el-container>
</template>

<script>
import { ref } from 'vue'
import { Monitor, Collection, Switch, InfoFilled, Operation, Location, Connection } from '@element-plus/icons-vue'

export default {
  name: 'App',
  components: {
    Monitor,
    Collection,
    Switch,
    InfoFilled,
    Operation,
    Location,
    Connection
  },
  setup() {
    const showAboutDialog = ref(false)
    const showAbout = () => {
      showAboutDialog.value = true
    }
    return {
      showAboutDialog,
      showAbout
    }
  }
}
</script>

<style>
:root {
  --primary-gradient: linear-gradient(135deg, #24243e 0%, #302b63 50%, #0f0c29 100%);
  --secondary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  --hover-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  --transition-cubic: cubic-bezier(0.4, 0, 0.2, 1);
}

body {
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  background-color: #f5f7fa;
}

.app-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.app-header {
  padding: 0;
  background: var(--primary-gradient);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.logo {
  color: #fff;
  font-size: 1.5rem;
  font-weight: bold;
  margin-right: 2rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.nav-menu {
  border: none !important;
  flex: 1;
  display: flex !important;
}

.el-menu--horizontal {
  border-bottom: none !important;
}

.el-menu--horizontal > .el-menu-item {
  height: 60px;
  line-height: 60px;
  border: none !important;
  padding: 0 20px !important;
}

.el-menu-item {
  flex-shrink: 0 !important;
  white-space: nowrap !important;
}

.el-menu-item .el-icon {
  margin-right: 5px;
  font-size: 1.2em;
}

.app-main {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.app-footer {
  background-color: #fff;
  border-top: 1px solid #e4e7ed;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.03);
}

.footer {
  text-align: center;
  color: #606266;
  font-size: 14px;
}

.footer p {
  margin: 5px 0;
}

/* 卡片样式 */
.el-card {
  border-radius: 8px;
  border: none;
  box-shadow: var(--card-shadow) !important;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.el-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.15) !important;
}

/* 按钮样式 */
.el-button {
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.el-button--primary {
  background: var(--primary-gradient);
  border: none;
}

.el-button--primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 输入框样式 */
.el-input__inner {
  border-radius: 6px;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 关于按钮样式 */
.about-btn {
  color: #fff !important;
  font-size: 14px !important;
  margin-left: auto !important;
  padding: 0 15px !important;
  height: 60px !important;
  display: flex !important;
  align-items: center !important;
}

.about-btn:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.about-btn .el-icon {
  margin-right: 5px;
}

/* 关于对话框样式优化 */
.about-dialog {
  border-radius: 12px;
}

.about-dialog .el-dialog__header {
  margin: 0;
  padding: 20px 20px 0;
  text-align: center;
}

.about-dialog .el-dialog__title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.about-dialog .el-dialog__body {
  padding: 30px;
}

.about-content {
  text-align: center;
}

.about-header {
  margin-bottom: 30px;
}

.about-header .logo-icon {
  color: var(--el-color-primary);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 15px;
}

.about-header h2 {
  margin: 10px 0;
  font-size: 24px;
  color: #303133;
}

.version {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.about-body h3 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 20px;
  font-weight: 600;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin: 20px 0;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  background: #f5f7fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.feature-item:hover {
  transform: translateX(5px);
  background: #ecf5ff;
}

.feature-item .el-icon {
  font-size: 20px;
  color: var(--el-color-primary);
}

.feature-item span {
  font-size: 15px;
  color: #606266;
}

.about-footer {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.about-footer p {
  margin: 5px 0;
  color: #909399;
  font-size: 14px;
}

/* 动画效果 */
.el-dialog__wrapper {
  transition: all 0.3s ease-out;
}

.el-dialog {
  transform: scale(0.9);
  transition: all 0.3s ease-out;
}

.el-dialog__wrapper.dialog-fade-enter-active .el-dialog,
.el-dialog__wrapper.dialog-fade-leave-active .el-dialog {
  transform: scale(1);
}

/* 移动端底部导航 */
.mobile-footer {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.mobile-nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 100%;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #606266;
  text-decoration: none;
  font-size: 12px;
  padding: 4px 0;
  flex: 1;
  cursor: pointer;
}

.nav-item .el-icon {
  font-size: 20px;
  margin-bottom: 2px;
}

.nav-item.active {
  color: var(--el-color-primary);
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .mobile-footer {
    background: #1d1e1f;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
  }

  .nav-item {
    color: #a8abb2;
  }
}

@media screen and (max-width: 768px) {
  .header-content {
    padding: 0 10px;
  }

  .logo {
    font-size: 1.2rem;
    margin-right: 1rem;
  }

  .nav-menu {
    display: none !important;
  }

  .about-btn {
    display: none !important;
  }

  .mobile-footer {
    display: block;
  }

  /* 为底部导航腾出空间 */
  .app-main {
    padding-bottom: 60px;
  }

  /* 调整对话框样式 */
  .about-dialog {
    width: 90% !important;
    margin: 0 auto;
  }

  .feature-list {
    gap: 10px;
  }

  .feature-item {
    padding: 8px 15px;
  }
}

.update-list {
  margin: 10px 0;
}

.update-item {
  margin-bottom: 15px;
}

.version-tag {
  font-weight: bold;
  color: var(--el-color-primary);
  margin-bottom: 5px;
}

.update-item ul {
  margin: 0;
  padding-left: 20px;
}

.update-item li {
  margin: 3px 0;
}
</style> 