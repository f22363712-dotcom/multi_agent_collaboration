# 多 Coding Agent 协同工作框架 (agy-flow) 使用手册 (v2)

本手册详细介绍了 `agy-flow` 全局协同框架的设计理念、配置规范、命令行使用以及针对 **Claude Code**、**Antigravity** 和 **Codex** 三个不同 Agent 的具体协同开发指南。

---

## 一、 全局架构与设计理念

`agy-flow` 采用 **“项目根路径向上检索”** 机制（类似于 Git 工作原理），支持您在项目内的任意子目录直接调用全局指令，使其成为您整个开发流程中无感知的“开发基座”：

*   **全局命令行**：支持在任意终端直接输入 `agy-flow <command>` 启动，无需切换到特定安装目录。
*   **自适应项目查找**：当您在项目的任何子目录（如 `D:\my-project\src\components`）执行 `agy-flow status` 时，工具会自动向上遍历父级目录寻找 `.agents` 文件夹，锁定当前激活的项目根目录。
*   **Git Worktree 隔离机制**：各个 Agent 分配在隔离的临时目录（如 `../{project_name}_worktrees/task-00X`）中，确保并发开发时代码互不污染、互不冲突。

---

## 二、 全局安装与配置说明

### 1. 全局命令配置 (Windows PATH)
系统已经为您在 `D:\tools` 目录下创建了 `agy-flow.bat` 包装脚本，并将 `D:\tools` 成功添加至您的用户环境变量 `Path` 中。

在您**重新打开命令提示符（CMD）或 VS Code 终端**后，您可以在全局任何地方直接调用：
```bash
agy-flow --help
```

### 2. 默认配置文件规范
配置文件位于每个项目根目录的 `.agents/config.json` 下，默认采用**相对路径**解析隔离工作区，确保不同项目之间的隔离区不发生混淆：

```json
{
    "project_name": "您的项目名",
    "worktrees_dir": "../multi_agent_worktrees",
    "agents": {
        "claude": {
            "cli_command": "claude",
            "default_args": ["-p", "--allowedTools", "Edit,Read,Bash", "--permission-mode", "dontAsk"],
            "guide_file": "CLAUDE.md"
        },
        "antigravity": {
            "guide_file": ".agents/AGENTS.md"
        },
        "codex": {
            "interactive": true
        }
    }
}
```

---

## 三、 全局核心指令指南

您可以在任意文件夹下执行以下指令：

### 1. 初始化新项目
在您的任意项目根目录下（如您的新开发文件夹内）执行，将该目录初始化为 `agy-flow` 项目（自动创建 `.agents/` 看板与配置并执行 `git init`）：
```bash
agy-flow init
```

### 2. 创建新开发任务
自动在项目根目录生成任务文件并追加至看板：
```bash
agy-flow create "任务标题" --agent <claude|antigravity|codex>
```

### 3. 查看当前项目进度
展示当前项目的所有任务状态：
```bash
agy-flow status
```

### 4. 启动任务并拉起隔离区
```bash
agy-flow start <task-id>
```

### 5. 在隔离区完成开发后提审
```bash
agy-flow submit <task-id> [--test-cmd "测试指令"]
```

### 6. 合并代码并销毁隔离区
```bash
agy-flow merge <task-id>
```

---

## 四、 三 Agent 协同实操流

1.  **纯逻辑与算法测试任务 -> 指派给 Claude Code (`--agent claude`)**
    *   在主目录下运行 `agy-flow start task-00X`。
    *   在专属隔离工作区运行 `claude -p "Read CLAUDE.md and implement the task."`。
    *   通过 `agy-flow submit` 完成测试与提审。
2.  **视觉、走查与多模态审核任务 -> 指派给 Antigravity (`--agent antigravity`)**
    *   在主目录下运行 `agy-flow start task-00X`。
    *   直接在您当前的 Antigravity 聊天窗口中，指示我去处理对应的 Worktree 目录。
    *   我会在该隔离目录内跑命令、写代码、用浏览器检查 UI，完成后通知您。通过 `agy-flow submit` 提交。
3.  **IDE 级人机手动调试任务 -> 指派给 Codex (`--agent codex`)**
    *   在主目录下运行 `agy-flow start task-00X`。
    *   **自动运行**：系统检测到 Codex 任务启动后，会**自动在隔离工作区拉起一个新的 VS Code 窗口**。
    *   **开发与热键提交**：直接在弹出的 VS Code 窗口中配合 Codex 编写代码。完成后，按 **`Ctrl+Shift+B`**，选择 `agy-flow: Submit This Task` 即可完成一键提交提审，无需手动在终端输入 submit。
