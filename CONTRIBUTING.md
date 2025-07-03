# 贡献指南

> 🙏 感谢您对技术文章工具项目集合的关注和贡献！

## 📋 目录

- [贡献流程](#贡献流程)
- [开发规范](#开发规范)
- [提交规范](#提交规范)
- [文档规范](#文档规范)
- [测试规范](#测试规范)
- [代码审查](#代码审查)
- [版本发布](#版本发布)
- [问题反馈](#问题反馈)

## 贡献流程

### 1. 准备工作

1. **Fork 项目仓库**：访问 [项目主页](https://github.com/username/notion_storage)，点击右上角的 Fork 按钮
2. **克隆到本地**：
   ```bash
   git clone https://github.com/YOUR_USERNAME/notion_storage.git
   cd notion_storage
   ```
3. **添加上游仓库**：
   ```bash
   git remote add upstream https://github.com/username/notion_storage.git
   ```

### 2. 创建分支

为每个新功能或修复创建独立的分支：

```bash
# 同步主分支
git checkout main
git pull upstream main

# 创建新分支
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/issue-description
```

### 3. 开发流程

1. **遵循项目规则**：查看 `.trae/rules/project_rules.md` 了解项目开发规则
2. **实现功能或修复**：按照规范编写代码和文档
3. **本地测试**：确保代码通过所有测试
4. **提交更改**：遵循提交规范提交代码

### 4. 提交 Pull Request

1. **推送到 Fork 仓库**：
   ```bash
   git push origin feature/your-feature-name
   ```
2. **创建 Pull Request**：访问 GitHub 仓库页面，点击 "Compare & pull request"
3. **填写 PR 信息**：提供清晰的标题和详细描述
4. **等待审查**：项目维护者会审查您的 PR 并提供反馈

## 开发规范

### 代码风格

- **Python 代码**：遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
- **JavaScript 代码**：遵循 [Airbnb JavaScript 风格指南](https://github.com/airbnb/javascript)
- **使用工具**：
  - Python: Black, Ruff, MyPy
  - JavaScript: ESLint, Prettier

### 项目结构

- 遵循项目现有的目录结构
- 新项目应创建独立的目录，包含完整的文档和测试
- 参考 `.trae/rules/project_rules.md` 中的项目组织结构规则

## 提交规范

### 提交信息格式

```
<类型>(<范围>): <简短描述>

<详细描述>

<关联的 issue>
```

### 类型

- **feat**: 新功能
- **fix**: 修复 Bug
- **docs**: 文档更新
- **style**: 代码风格调整（不影响功能）
- **refactor**: 代码重构
- **perf**: 性能优化
- **test**: 测试相关
- **chore**: 构建过程或辅助工具变动

### 示例

```
feat(ai-decision-framework): 添加新的评估维度

增加了用户体验评估维度，包含3个指标：
- 交互复杂度
- 响应时间
- 学习曲线

Resolves #123
```

## 文档规范

### README.md

- 每个项目必须有完整的 README.md
- 遵循项目规则中的 README.md 写作要求
- 包含项目背景、安装步骤、使用示例等必要信息

### 代码注释

- 为所有公共 API 提供文档字符串
- 为复杂逻辑添加注释
- 使用清晰的变量和函数命名

## 测试规范

### 测试要求

- 所有新功能必须有对应的测试
- 修复 Bug 时应添加回归测试
- 测试覆盖率应保持在 80% 以上

### 测试工具

- Python: pytest
- JavaScript: Jest

## 代码审查

### 审查标准

- 代码质量和风格
- 功能完整性
- 测试覆盖率
- 文档完善度
- 性能考虑

### 审查流程

1. 提交者创建 PR
2. 维护者进行代码审查
3. 提交者根据反馈进行修改
4. 维护者批准并合并 PR

## 版本发布

### 版本号规范

遵循 [语义化版本控制](https://semver.org/lang/zh-CN/)：

- **主版本号**：不兼容的 API 变更
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

### 发布流程

1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建发布标签
4. 发布版本

## 问题反馈

### 提交 Issue

- 使用 Issue 模板
- 提供详细的问题描述
- 包含复现步骤
- 附上相关日志或截图

### Issue 类型

- **Bug 报告**：描述发现的问题
- **功能请求**：提出新功能建议
- **文档改进**：文档相关的建议
- **性能问题**：性能相关的问题

---

感谢您的贡献！如有任何问题，请通过 Issue 或邮件联系项目维护者。