# GitHub 加速下载工具

一键生成 GitHub 文件加速链接的小工具，解决国内 GitHub 下载慢的问题。

## 功能

- 输入 GitHub 原始下载链接 → 自动生成 `gh-proxy.com` 加速链接
- **多节点支持**：内置 4 个加速节点，可随意切换
- **自定义节点**：输入任意代理地址
- **节点管理**：添加/删除自有节点
- **配置持久化**：自动保存到 `config.ini`
- **一键复制**：转换后自动复制到剪贴板

## 使用

### 直接运行（无需 Python）
下载 [Releases](https://github.com/cymylive/ghproxy-accelerator/releases) 中的 `ghproxy.exe`，双击运行。

### 从源码运行
```bash
pip install pyinstaller  # 仅打包需要
python ghproxy_gui.py
```

## 节点说明

| 节点地址 | 说明 |
|---------|------|
| `https://gh-proxy.com/` | Cloudflare 加速，默认节点 |
| `https://ghproxy.net/` | 国内常见代理 |
| `https://github.akams.cn/` | 另一个可用节点 |
| `https://ghproxy.cfd/` | 备用节点 |

## 截图

![screenshot](./screenshot.png)

## 打包
```bash
pyinstaller --onefile --noconsole --name ghproxy ghproxy_gui.py
```

## License

MIT
