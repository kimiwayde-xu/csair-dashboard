# CLAUDE.md - 宣传看板大屏项目

## 项目概述

**项目名称**: 2026年地服部宣传数据可视化看板
**项目路径**: `/Users/xuweijie/.qclaw/workspace/宣传看板大屏/vercel-deploy/`
**GitHub仓库**: https://github.com/kimiwayde-xu/csair-dashboard
**在线访问**: https://kimiwayde-xu.github.io/csair-dashboard/
**部署方式**: GitHub Pages
**访问方式**: 需要通过 HTTP 服务器访问(不能直接双击 HTML 文件)

---

## 技术栈

- **前端框架**: 原生 HTML + CSS + JavaScript(无框架)
- **图表库**: ECharts 5.x(CDN 加载)
- **数据加载**:
  - `data.json` - 图表数据(fetch 动态加载,带缓存破坏参数)
  - `photos.json` - 照片列表(fetch 动态加载,带缓存破坏参数)
- **部署平台**: GitHub Pages

---

## 文件结构

```
vercel-deploy/
├── index.html              # 主页面(~79KB,fetch动态加载data.json+articles.json)
├── data.json               # 图表数据(~13KB,fetch 动态加载,含版本号缓存)
├── articles.json           # 稿件明细数据(~89KB,12科室425篇,fetch动态加载,含版本号缓存)
├── photos.json             # 图片列表(24张图片)
├── photos/                 # 图片文件夹(24张 jpg/png)
├── generate_articles_json.py  # 稿件数据生成脚本(读取Excel 2026汇总表)
├── CLAUDE.md               # 本项目记忆文件(本文件)
├── .github/                # GitHub Pages 配置
└── .git/                   # Git 仓库
```

**根目录辅助文件**(不在仓库中但必不可少):
```
宣传看板大屏/
├── server.py            # Excel解析 + Web上传服务(桌面脚本Step1用parse_excel)
├── server_v2.py         # 废弃文件(功能已被server.py取代,桌面脚本用server.py)
├── generate_articles_json.py  # 在仓库vercel-deploy/中也有副本
├── run_tests.py         # 68项自动化测试(TDD套件)
├── update_dashboard.sh  # 一键更新脚本(旧版,推荐用桌面脚本)
└── 宣传看板数据.xlsx    # 数据源(桌面脚本读取固定路径外置硬盘)
```

**已删除文件**:
- `index_new.html` - 旧模板文件(2026-06-04删除)
- `add_gallery.py` - 旧添加Gallery工具(2026-06-04删除)

---

## 核心功能

### 1. 数据可视化图表
- **平台分布**: 饼图(内部媒体、行业媒体、主流媒体、公众号、视频号、协助宣传)
- **月度科室排名**: 柱状图(前三名金银铜高亮,可切换年份+月份,点击柱状图查看稿件详情弹窗)
- **全年科室排名**: 柱状图(前三名带🥇🥈🥉标签 + 闪烁动画,点击柱状图查看稿件详情弹窗)
- **科室同比分析**: 柱状图(增长前三绿色、下降前三红色,带阴影高亮)
- **月度趋势对比**: 折线图(2025 vs 2026)

### 2. 指标卡片
- **总稿件**: 全年累计
- **月均**: 平均每月稿件数
- **当月**: 当前选中月份稿件数
- **同比**: 与去年同期对比(绿色/红色)

### 3. 登稿视窗(原"宣传照片")
- **位置**: 页面底部,全宽卡片(`grid-column: span 4`)
- **数据源**: `photos.json` fetch 动态加载
- **切换效果**: 淡入淡出(CSS transition opacity 0.8s ease-in-out)
- **自动播放**: 5秒切换
- **手动控制**: 左右箭头按钮 + 底部指示点
- **悬停暂停**: 鼠标悬停暂停,离开恢复自动播放

### 4. 控制面板
- **年份选择器**: 2026年、2025年(硬编码)
- **月份选择器**: 动态生成(根据数据中有数据的月份)
  - 自动选中最后一个有数据的月份
  - 年份切换时自动重新生成月份列表
- **刷新按钮**: 手动刷新页面数据
- **实时时钟**: 页面右上角 Header,格式 `toLocaleString('zh-CN')`
- **版本号缓存**: localStorage缓存data.json和articles.json,版本相同则复用,减少等待
- **骨架屏**: 首次加载或缓存未命中时显示骨架屏动画,数据就绪后平滑过渡
- **月份动态选择**: 从data.json读取实际有数据的月份,自动选中最后一月

---

## 数据更新流程

### 方式一:使用桌面工具(推荐)

#### 1. 更新图表数据
双击运行:`~/Desktop/更新宣传看板.command`
- 解析Excel文件(固定路径:`/Volumes/way的固态/工作/2026/宣传/2026部门宣传数据可视化看板.xlsx`)
- **Step 1**: `server.parse_excel()` → 生成 `data.json` (动态读取"数据源"工作表列E科室名,current_month自动检测)
- **Step 2**: `generate_articles_json.py` → 生成 `articles.json` (动态读取"2026汇总表"第2行表头,12科室名与data.json完全一致)
- **Step 3**: git add → git commit → git push (仅推送data.json + articles.json + generate_articles_json.py)
- 网页通过fetch动态加载数据,无需修改HTML

##### 数据一致性保证(2026-06-08修复)
- `server.py` 和 `generate_articles_json.py` 均动态读取Excel(不硬编码科室名)
- `generate_articles_json.py` 的 `read_dept_names()` 读取2026汇总表第2行列6-17作为键名
- `server.py` 读取"数据源"工作表列E原始值(废弃旧版DEPT_MAP硬编码)
- 两文件输出科室名完全一致(验证通过 68项测试)

#### 2. 更新照片
双击运行:`~/Desktop/更新宣传照片.command`
- 扫描 `vercel-deploy/photos/` 文件夹
- 自动生成 `photos.json`
- 自动 Git 提交推送(包含新照片文件)

### 方式二:手动更新

#### 更新图表数据
```bash
cd /Users/xuweijie/.qclaw/workspace/宣传看板大屏
./update_dashboard.sh [Excel文件路径]
```

#### 新增/删除图片
1. 将图片放入 `photos/` 文件夹
2. 运行 `generate_photos_json.py` 生成 `photos.json`
3. Git 提交推送:
   ```bash
   cd /Users/xuweijie/.qclaw/workspace/宣传看板大屏/vercel-deploy
   git add photos.json photos/
   git commit -m "更新照片"
   git push
   ```

---

## 本地测试

### 启动本地服务器
```bash
cd /Users/xuweijie/.qclaw/workspace/宣传看板大屏/vercel-deploy
python3 -m http.server 8080
```

### 访问
浏览器打开:`http://localhost:8080`

⚠️ **注意**: 不能直接双击 `index.html` 文件,必须通过 HTTP 服务器访问,否则 `fetch('data.json')` 和 `fetch('photos.json')` 会被浏览器阻止(CORS 策略)。

---

## 关键设计决策

### 1. 数据完全动态化(2026-06-04 最终实现)
- **现状**: `index.html` 通过 `fetch('data.json')` 动态加载数据
- **好处**: 更新数据只需修改 `data.json`,无需修改 HTML
- **缓存破坏**: fetch 请求带时间戳参数 + `cache: 'no-store'`
- **关键代码**:
  ```javascript
  let dashboardData = null;
  
  async function loadData() {
      // 1. 先从localStorage读取缓存（快速显示）
      const cachedData = localStorage.getItem('dashboardData');
      const cachedVersion = localStorage.getItem('dashboardDataVersion');
      if (cachedData) {
          dashboardData = JSON.parse(cachedData);
          hideSkeleton();
          showContent();
      }
      // 2. 后台检查更新
      const response = await fetch('data.json?t=' + Date.now(), { cache: 'no-store' });
      const newData = await response.json();
      // 3. 对比版本号
      const newVersion = \`\${newData.summary.total_articles}-\${newData.summary.monthly_avg}\`;
      if (newVersion !== cachedVersion) {
          localStorage.setItem('dashboardData', JSON.stringify(newData));
          localStorage.setItem('dashboardDataVersion', newVersion);
          dashboardData = newData;
      }
      return true;
  }
  
  // 加载顺序: loadArticles() → loadData() → generateMonthOptions() → initCharts() → updateDashboard()
  window.addEventListener('DOMContentLoaded', async () => {
      await loadArticles();  // 优先加载稿件数据(click handler就绪)
      await loadData();
      generateMonthOptions();  // 动态生成月份选项(覆盖哨兵值)
      initCharts();
      updateDashboard();
      loadPhotos();
  });
  ```

### 2. 月份选择器动态生成(2026-06-02 新增)
- **逻辑**: 从 `data.json` 读取该年份所有月份
- **智能选择**: 默认选中最后一个有数据的月份(total > 0)
- **联动**: 年份切换时自动重新生成月份列表

### 3. 照片轮播独立加载
- **方案**: `photos.json` 独立管理,通过 `fetch('photos.json')` 动态加载
- **好处**: 更新图片不影响图表代码

### 4. 前三名高亮
- **月度排名**: 金银铜渐变色 + 阴影发光
- **全年排名**: 🥇🥈🥉 emoji 标签 + 闪烁动画(1.5s 间隔)
- **同比分析**: 增长前三绿色阴影、下降前三红色阴影
- **柱状图可点击**: 查看对应科室/月份的稿件详情弹窗

### 5. Git 自动追踪照片文件(2026-06-02 修复)
- **问题**: `git add` 只添加 `photos.json`,不添加 `photos/` 文件夹
- **修复**: 改为 `git add data.json photos.json photos/`
- **教训**: 更新配置文件 ≠ 更新实际资源文件

### 6. 响应式布局(2026-06-02 新增)
- **断点设计**: 6个响应式断点(>1400px、1200-1400px、992-1199px、768-991px、576-767px、<576px)
- **自适应布局**: Dashboard卡片自动调整列数(4列 → 3列 → 2列 → 1列)
- **字体自适应**: 标题、数值、图表文字根据屏幕大小动态调整
- **图表高度自适应**: 300px(正常)→ 260px(平板)→ 250px(手机)→ 220px(小屏)
- **控制面板优化**: 大屏水平排列,手机垂直堆叠
- **触摸优化**: 手机端按钮、控件大小适中,易于点击
- **横轴信息完整显示**: 小屏幕单列布局,确保12个科室名称完整显示

### 7. 骨架屏加载优化(2026-06-08 新增)
- **触发条件**: 首次访问(无缓存)或数据已更新(版本号不一致)
- **缓存命中**: localStorage缓存数据时秒开,不显示骨架屏
- **动画效果**: 波纹动画(1.5s循环,从左到右扫过)
- **过渡**: 骨架屏淡出0.3s → 内容淡入0.3s
- **响应式**: 骨架屏结构适配所有设备(1-4列)
- **版本号缓存**: `dashboardDataVersion` + `articlesDataVersion` 两个独立缓存键

### 8. 柱状图点击查看稿件详情(2026-06-05/08 新增)
- **触发**: 点击月度或全年科室排名柱状图
- **弹窗内容**: 该科室该月所有稿件,含标题+链接+发布时间
- **数据源**: `articles.json`(425篇稿件)
- **科室匹配**: 动态读取Excel表头,与data.json完全一致
- **加载顺序**: `loadArticles()` → `loadData()` → `initCharts()`,确保data就绪

---

## 桌面工具

### 工具列表
1. `~/Desktop/更新宣传看板数据.command` - 上传 Excel 更新数据
2. `~/Desktop/更新宣传照片.command` - 扫描照片文件夹更新照片列表

### 工具原理
- **Python 服务**: `server_v2.py`(端口 8765)
- **Excel 解析**: 使用 `openpyxl` 库
- **照片扫描**: `generate_photos_json.py`
- **Git 自动化**: 自动提交推送

---

## 已知问题与解决方案

### Q1: 本地打开 HTML 显示"数据加载错误"
**原因**: 直接双击 HTML 文件(file:// 协议),浏览器阻止 fetch 请求
**解决**: 通过 HTTP 服务器访问(`python3 -m http.server 8080`)

### Q2: 照片更新后网页不显示新照片
**原因**: `git add` 只添加了 `photos.json`,未添加 `photos/` 文件夹
**解决**: 已修复,现在会自动添加 `photos/` 文件夹

### Q3: 年份选择器硬编码
**现状**: 年份选择器硬编码为 2025、2026
**影响**: 2027年需手动修改 HTML
**状态**: 已知,用户决定暂时不改

### Q4: resize监听器可能重复注册
**问题**: 每次调用initCharts()会添加新的resize监听器
**影响**: 长时间使用可能积累多个监听器
**状态**: 已部分优化(platformChart使用命名函数)，但其他图表仍使用匿名函数

### Q5: photos文件夹包含两种命名格式
**现象**: 文件夹内有"微信图片_..."和"00fa2e..."两种命名格式
**影响**: 无影响，photos.json已包含所有24张图片
**建议**: 可统一命名格式便于管理

### Q6: server_v2.py 已废弃
**现状**: 功能已被server.py取代,桌面脚本只使用server.py
**影响**: 可删除,但误删可能性低,保留即可

---

## 未来优化方向(可选)

1. ~~**加载动画**: 数据加载时显示 loading 状态~~ (✅ 已实现:骨架屏)
2. **年份选择器动态化**: 根据当前真实年份生成年份选项
3. **图片懒加载**: 当前22张图片全量预加载,可优化为按需加载
4. **自动刷新功能**: 添加定时刷新(如每30秒),适合大屏展示场景
5. **导出功能**: 看板截图/数据导出

---

## 重要提示

- ✅ **已完成的功能**:
  - 5个 ECharts 图表(平台分布、月度排名、全年排名、同比分析、月度趋势)
  - 指标卡片(总稿件、月均、当月、同比)
  - 登稿视窗(原"宣传照片",fetch photos.json + 自动播放 + 手动控制 + 悬停暂停)
  - 控制面板(年份选择器 + 月份动态选择器 + 刷新按钮)
  - 实时时钟
  - 前三名高亮(金银铜色 + emoji + 闪烁动画)
  - Bug修复(平台分布图resize错误、闪烁动画内存泄漏、photos.json同步)
  - 数据完全动态化(data.json + articles.json + 版本号缓存)
  - 桌面更新工具(Excel上传 + 照片扫描)
  - Git 自动化提交推送
  - GitHub Pages 在线访问
  - 响应式布局(支持桌面/平板/手机多设备自适应)
  - **骨架屏加载优化**(2026-06-08)
  - **柱状图点击查看稿件详情**(2026-06-08修复)
  - **科室名一致性**(动态读取Excel表头,不再硬编码,2026-06-08)
  - **currentMonth动态检测**(2026-06-08)
  - **自动化测试套件** run_tests.py(68项,2026-06-08)

- ⚠️ **待改进**:
  - [ ] 年份选择器改为动态生成(根据当前真实年份)
  - [ ] resize监听器重复注册问题(建议使用命名函数或once:true)
  - [ ] server_v2.py 已废弃,可考虑删除

---

## 联系方式

**项目负责人**: 徐伟杰  
**项目位置**: `/Users/xuweijie/.qclaw/workspace/宣传看板大屏/vercel-deploy/`  
**最后更新**: 2026-06-08 10:35 GMT+8

---

## 最近更新日志

### 2026-06-08 10:35 - TDD 架构清理 + 骨架屏 + 详情修复

**新增功能**:
1. **骨架屏加载优化** — 首次访问/数据更新时显示波纹加载动画,缓存命中时秒开跳过。
   Commit: `5992dd8` - "feat: 添加骨架屏加载优化"
2. **柱状图点击查看稿件详情** — 点击月度/全年科室排名柱状图,弹窗显示该科室该月所有稿件(含链接)。
   Commit: `cf3b275` - "fix: 柱状图点击无稿件详情"
3. **自动化测试套件** — `run_tests.py`,68项测试覆盖数据完整性/Excel验证/前端检查/架构扫描。

**Bug修复**:
1. **科室名不匹配(根因)** — `generate_articles_json.py` 原用两套硬编码映射(EXCEL_COL_TO_DEPT + DEPT_MAPPING),
   与实际Excel表头不一致,导致3个科室错配。
   ★ 修复:删掉硬编码映射,新增`read_dept_names()`动态读取Excel第2行表头。
   Commit: `9be3357` - "fix: 科室名称不匹配的根因修复"
2. **index.html currentMonth=5硬编码** — 改为哨兵值0,由`generateMonthOptions()`自动检测最后有数据月份。
3. **server.py current_month:5硬编码** — 改为`datetime.now().month`,动态匹配当前月份。
4. **server.py DEPT_MAP误导性硬编码** — 移除,直接读"数据源"工作表列E原始值。
5. **datetime局部import冲突** — 修正:改为全局datetime+仅timedelta局部import。

**架构清理**:
- server.py: DEPT_MAP移除、current_month动态化、datetime导入修复
- data.json: 重新生成(current_month=6)
- 桌面脚本完整性确认: Step1(data.json)+Step2(articles.json) 两文件科室名100%一致 ✅

**Git提交**: `2c7cfd3` - "fix: 架构清理 + 动态月份检测"

### 2026-06-08 11:13 - DEPT_NAME_MAP 回归Bug修复

**问题**: 浦东高端客服室/虹桥值机室/虹桥高端客服室 点击柱状图无稿件详情弹窗。

**根因**: 10:25修复了generate_articles_json.py科室名根因(动态读取Excel表头)后,
articles.json和data.json的科室名已100%一致,但前端DEPT_NAME_MAP丢失删除,仍在做反向映射:
- `浦东高端客服室→浦东高端服务室` ❌ (articles.json已用正确名浦东高端客服室)
- `虹桥值机室→虹桥值机` ❌
- `虹桥高端客服室→虹桥高端服务室` ❌

**修复**: DEPT_NAME_MAP清空为`{}`,直接用原科室名查找。

**经验教训**: 修根因后必须全局搜索所有依赖该根因的workaround代码,逐一验证清理。

**Git提交**: `5c9b5db` - "fix: 删除DEPT_NAME_MAP旧名映射"

**测试**: 69项全通过 ✅ (新增T7: DEPT_NAME_MAP无旧名映射)

### 2026-06-08 11:17 - 全量审计 + 架构清理

**审计发现的问题**:
1. **server.py current_month_platform死字段** — 空的platform分布对象写入data.json,
   前端从未使用。已有platform_distribution提供完整数据。
   → 移除全部3处引用
2. **handle_deploy使用旧架构** — Web UI部署仍用正则替换index.html的旧方法,
   不会推送data.json/articles.json,部署后前端无变化。
   → 改为: copy data.json + 运行generate_articles_json.py → git push data.json+articles.json

**验证**:
- `current_month_platform in data`: False ✅ (已清除)
- 桌面脚本端到端: 12科室名100%一致 ✅
- 全部测试: 69项通过 ✅

**Git提交**: 待本次推送

### 2026-06-04 09:05 - 架构优化与清理
**修复内容**:
1. **修复数据不更新问题** - 改为fetch动态加载data.json(之前硬编码在HTML中)
2. **修复图片轮播被覆盖** - 修改更新脚本,只更新data.json,不修改index.html
3. **删除旧模板文件** - 删除`index_new.html`和`add_gallery.py`

**架构演进**:
- ❌ 旧架构: 模板替换(`index_new.html` + `DATA_PLACEHOLDER`)
- ✅ 新架构: 动态加载(`fetch('data.json')`)

**Git提交**: 
- `fix: 改为fetch动态加载data.json，解决数据不更新问题`
- `chore: 删除旧模板文件index_new.html（已改为动态加载data.json）`

### 2026-06-03 10:14 - Bug修复
**修复内容**:
1. **平台分布图resize处理错误** - 修正为正确的option结构
2. **全年科室排名闪烁动画内存泄漏** - 添加beforeunload清除定时器
3. **photos.json重新生成** - 包含全部24张图片(修正微信命名+哈希命名混合问题)

**Git提交**: `fix: 修复bug并更新photos.json`

### 2026-06-03 09:46 - 图表字体响应式适配
**优化内容**:
- 所有图表横轴字体根据屏幕大小动态调整(桌面12px → 手机9-11px)
- 手机端横轴旋转角度加大到45°，避免重叠
- 窗口大小变化时自动重新应用字体配置

**Git提交**: `feat: 图表字体大小响应式适配，横轴文字完整显示`

### 2026-06-03 09:41 - 修复图表标题月份不同步bug
**问题**: 页面默认显示6月，但图表标题显示"5月"
**解决**: 在DOMContentLoaded中initCharts()后添加updateDashboard()调用

**Git提交**: `fix: 修复页面加载时图表标题月份不同步的bug`