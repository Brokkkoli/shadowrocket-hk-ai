# 香港 AI Only 自动更新

固定导入地址：

https://raw.githubusercontent.com/Brokkkoli/shadowrocket-hk-ai/main/Howard-HK-AI-Only.conf

香港日常使用：指定 AI 代理，其余直连。PROXY 使用 Shadowrocket 首页所选节点。

## 两个更新环节

1. GitHub 每天香港时间约 08:23（实际可能延迟）获取 OpenAI 官方语音地址，校验后生成 Howard-HK-AI-Only.conf。有变化才提交；下载或校验失败不修改旧配置。
2. Shadowrocket 从该固定地址定期下载配置，需要在手机开启“设置 → 配置 → 自动后台更新”，更新间隔建议 1 天；iOS“设置 → 通用 → 后台 App 刷新”也需允许 Shadowrocket。iOS 调度不保证精确到点，强制退出应用会影响后台更新。

自动维护范围是官方语音 IP。AI 域名规则保持在 config.template.conf 中，服务增加域名时仍需维护模板；系统不会自动发现所有新 AI 域名。模板更新后，生成流程会运行，手机再按自己的周期获取更新。

## 部署

在自己的 GitHub 账号创建独立公开仓库，默认分支 main。仅上传本文件包中的内容，不上传旧聊天记录、账号凭证、订阅地址、节点或私钥。启用 GitHub Actions 并运行 Refresh Hong Kong AI configuration。

生成程序使用 GITHUB_REPOSITORY 自动填写实际仓库的 update-url。生成结果验证通过后，使用该仓库中 Howard-HK-AI-Only.conf 的 Raw URL 导入 Shadowrocket。不要把模板作为配置导入。

仓库公开意味着这些通用路由规则与提交者 GitHub 身份关联；文件包没有节点或私人订阅。GitHub Actions 只获本仓库内容写入权限，用于提交生成配置。

如仓库长期没有活动导致定时工作流停用，需在 Actions 中重新启用。需要检查时查看最近一次工作流成功时间和生成文件的提交记录。

## 验证

已用随附审查中的官方语音快照验证生成过程，并检查危险网段输入被拒绝。上线后还必须验证工作流成功、Raw URL 可公开下载以及手机更新成功。线上运行状态以 GitHub Actions 最近一次执行结果为准。

配置自动更新设置参考：[社区使用手册](https://github.com/LOWERTOP/Shadowrocket#自动更新)。

官方语音源：[chatgpt-voice.json](https://openai.com/chatgpt-voice.json)。
