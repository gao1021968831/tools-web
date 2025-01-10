# IP工具集

一个功能强大的IP地址工具集合，提供多种IP地址相关的计算和转换功能。

## 项目结构

````

ip-tools/
├── frontend/                 # 前端项目目录
│   ├── src/
│   │   ├── api/             # API 接口
│   │   │   └── ip.js        # IP相关接口
│   │   ├── assets/          # 静态资源
│   │   │   └── styles/      # 样式文件
│   │   │       └── common.css
│   │   ├── components/      # 公共组件
│   │   ├── config/          # 配置文件
│   │   │   └── index.js     # 全局配置
│   │   ├── router/          # 路由配置
│   │   │   └── index.js
│   │   ├── utils/           # 工具函数
│   │   │   └── request.js   # axios 封装
│   │   ├── views/           # 页面组件
│   │   │   ├── NetworkCalc.vue    # 网段计算
│   │   │   ├── IpSummary.vue      # IP汇总
│   │   │   ├── IpConversion.vue   # IP转换
│   │   │   ├── IpFormat.vue       # IP格式转换
│   │   │   └── SubnetCalc.vue     # 子网划分
│   │   ├── App.vue          # 根组件
│   │   └── main.js          # 入口文件
│   ├── index.html           # HTML 模板
│   ├── package.json         # 依赖配置
│   └── vite.config.js       # Vite 配置
│
├── backend/                  # 后端项目目录
│   ├── utils/               # 工具函数
│   │   └── ip_tools.py      # IP处理工具
│   ├── app.py               # 主应用
│   └── requirements.txt     # Python 依赖
│
├── .gitignore               # Git 忽略配置
├── README.md                # 项目说明
└── LICENSE                  # 许可证


````

## 功能特性

- 🌐 网段计算
  - IP子网计算
  - 可用地址范围计算
  - 私有地址识别
  - 网络地址和广播地址计算

- 📊 IP汇总
  - 多个IP地址/网段汇总
  - 智能合并连续地址
  - 支持批量处理

- 🔄 IP转换
  - IPv4转IPv6
  - IPv6转IPv4
  - 支持批量转换
  - 自定义IPv6前缀

- 🔀 IP格式转换
  - 十进制 ↔ 二进制
  - 十进制 ↔ 十六进制
  - 掩码 ↔ CIDR
  - 批量转换支持

- 📐 子网划分
  - 按子网数量划分
  - 按主机数量划分
  - 自动计算最优划分
  - 显示详细子网信息

## 技术栈

### 前端
- Vue 3
- Element Plus
- Vite
- Vue Router
- Axios

### 后端
- Python
- Flask
- ipaddress

## 开发环境

### 前端依赖
```json
{
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.0.0",
    "element-plus": "^2.5.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-vue": "^5.0.0"
  }
}
```

### 后端依赖
```
Flask==3.0.0
flask-cors==4.0.0
ipaddress==1.0.23
```

## 部署要求

### 前端
- Node.js >= 14.0.0
- npm >= 6.0.0

### 后端
- Python >= 3.8
- pip

## 快速开始

1. 克隆仓库
```bash
git clone https://github.com/yourusername/ip-tools.git
cd ip-tools
```

2. 前端设置
```bash
cd frontend
npm install
npm run dev
```

3. 后端设置
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## 使用说明

### 网段计算
1. 输入IP地址和子网掩码
2. 点击"计算"按钮
3. 查看详细的网段信息

### IP汇总
1. 输入多个IP地址或网段（每行一个）
2. 点击"汇总"按钮
3. 获取优化后的地址范围

### IP转换
1. 选择转换方向（IPv4转IPv6或IPv6转IPv4）
2. 输入需要转换的IP地址列表
3. 对于IPv4转IPv6，需要提供IPv6前缀
4. 点击"转换"按钮

### IP格式转换
1. 选择转换类型
2. 输入需要转换的IP地址列表
3. 点击"转换"按钮
4. 可以复制转换结果

### 子网划分
1. 输入主网段（如：192.168.0.0/24）
2. 选择划分方式：
   - 按子网数量：指定需要划分的子网数量
   - 按主机数量：指定每个子网需要的主机数
3. 输入相应的数值
4. 点击"计算"按钮
5. 查看划分结果，包括：
   - 子网地址
   - 子网掩码
   - 可用主机数
   - 可用地址范围

## 版本历史

### v1.0.0 (2024-03-xx)
- 🎉 首次发布
- ✨ 实现网段计算功能
- ✨ 实现IP汇总功能
- ✨ 实现IPv4/IPv6转换功能

### v1.1.0 (2024-03-xx)
- ✨ 新增IP格式转换功能
- 🎨 优化移动端适配
- 🐛 修复已知问题
- ⚡️ 性能优化

### v1.2.0 (2024-03-xx)
- ✨ 新增子网划分功能
- 🎨 优化表格显示
- ⚡️ 改进计算性能
- 📱 完善移动端适配

## 待实现功能
- [ ] IP地址批量Ping检测
- [ ] IP地址归属地查询
- [ ] 网络连通性诊断
- [ ] IP地址冲突检测

## 贡献指南

欢迎提交 Issue 和 Pull Request。在提交 PR 之前，请确保：

1. 代码风格符合项目规范
2. 添加必要的测试
3. 更新相关文档
4. 遵循语义化版本规范

## 许可证

[MIT License](LICENSE)

## 作者

- gcg

## 致谢

感谢所有为这个项目做出贡献的开发者。

这个合并后的 README：

1. 包含了完整的项目结构
2. 详细的功能说明
3. 完整的技术栈和依赖信息
4. 清晰的部署和使用指南
5. 版本历史记录
6. 贡献指南和许可信息

