# ima「微信沉淀库」入库操作（技术参考）

执行 SKILL.md 第 6 步「入库」时按本文件操作。先通过 `ima-mcp` skill 了解连接器选型与编排规则。

## 关键事实

- 默认目标库：**「微信沉淀库」**，knowledge_base_id = `7509177857476175`
  （勿凭记忆硬编码，若用户指定其他库，先查库/查可写库确认真实 id；多 IMA 连接器时写操作按 ima-mcp skill 的选型规则先确认连接器）
- 入库是**异步解析**：add_knowledge 成功 ≠ 立刻可检索，回执时如实告知"稍等片刻即可检索"

## 入库三步（缺一不可）

### 1. create_media

调 `mcp__ima-mcp__create_media`，参数：
- `content_type`: 卡片为 md 文件 → `text/markdown`
- `file_name`: 卡片文件名（如 `2026-09-26-主题.md`）
- `file_size`: **必须与文件实际字节数一致**（`wc -c` 确认）
- `knowledge_base_id`: 上面拿到的真实 id

返回 `media_id` + `cos_credential`。

### 2. COS 上传

⚠️ **直接把 cos_credential.token 当 Authorization 头会 403**。COS 要求用临时密钥（secret_id/secret_key/token）计算请求级签名，并把 token 放 `x-cos-security-token` 头。

使用本技能自带脚本（自动完成签名计算）：

```bash
# 1) 把 create_media 返回的 cos_credential 原样存为 JSON
#    <技能目录>/scripts/cos_credential.json（即 SKILL.md 同级 scripts/ 下）
# 2) 上传
python <本技能目录>/scripts/ima_upload.py <卡片md文件路径>
# 输出 HTTP 200 即成功；脚本位于技能捆绑的 scripts/ima_upload.py
```

脚本核心逻辑（备用/调试）：对 `put\n/<cos_key>\n\n\n` 取 SHA1，与 keyTime（`start_time;expired_time`）一起按 COS 签名算法用 secret_key 两次 HMAC-SHA1 生成 `q-sign-algorithm=sha1&q-ak=...&q-sign-time=...&q-key-time=...&q-header-list=&q-url-param-list=&q-signature=...`，PUT 到 `https://{bucket_name}.cos.{region}.myqcloud.com/{cos_key}`。

### 3. add_knowledge

调 `mcp__ima-mcp__add_knowledge`，传 `knowledge_base_id` + 第 1 步返回的 `media_id`。返回正常即入库成功。

## 失败兜底（对应硬性规则第 5 条）

- 工具执行错误（isError）：按错误文本纠正后重试一次
- 鉴权失败：提示用户到 WorkBuddy 设置页重连 ima 连接器，不要反复重试
- COS 上传失败 / add_knowledge 失败：把卡片存到本地「微信沉淀-待回传」文件夹，按 SKILL.md 回复格式告知路径与手动回传方法
- 批量导入部分失败：只对失败项重试一次，回执中报告成功/失败条数
