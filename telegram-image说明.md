# Telegraph-Image API 文档

## 项目简介

Telegraph-Image 是一个免费的图片托管解决方案，基于 Cloudflare Pages 和 Telegram API，提供无限图片存储和快速访问。

## API 端点

### 1. 上传 API

**端点**: `/upload`

**方法**: `POST`

**描述**: 上传图片/文件并获取访问链接

**请求格式**: `multipart/form-data`

**参数**:
- `file` (必填): 要上传的文件

**响应**:

成功:
```json
[
  {
    "src": "/file/{fileId}.{extension}"
  }
]
```

失败:
```json
{
  "error": "错误信息"
}
```

**示例**:
```bash
curl -X POST -F "file=@example.jpg" https://your-domain.pages.dev/upload
```

### 2. 文件访问 API

**端点**: `/file/{fileId}.{extension}`

**方法**: `GET`

**描述**: 直接访问上传的文件

**参数**:
- `fileId` (必填): 文件ID
- `extension` (必填): 文件扩展名

**响应**:
- 成功: 返回文件内容
- 失败: 可能返回错误页面或重定向

**示例**:
```
https://your-domain.pages.dev/file/AgACAgEAAxkDAAMDZt1Gzs4W8dQPWiQJxO5YSH5X-gsAAt-sMRuWNelGOSaEM_9lHHgBAAMCAANtAAM2BA.png
```

### 3. 管理 API

#### 3.1 列出所有文件

**端点**: `/api/manage/list`

**方法**: `GET`

**描述**: 列出所有上传的文件

**参数**:
- `limit` (可选): 每页返回的文件数量，默认100，最大1000
- `cursor` (可选): 分页游标
- `prefix` (可选): 文件前缀过滤

**响应**:
```json
{
  "keys": [
    {
      "name": "{fileId}.{extension}",
      "expiration": null,
      "metadata": {
        "TimeStamp": 1673984678274,
        "ListType": "None",
        "Label": "None",
        "liked": false,
        "fileName": "example.jpg",
        "fileSize": 102400
      }
    }
  ],
  "list_complete": true,
  "cursor": "optional-cursor"
}
```

#### 3.2 阻止文件

**端点**: `/api/manage/block/{id}`

**方法**: `POST`

**描述**: 将文件加入黑名单，阻止访问

**参数**:
- `id` (必填): 文件ID

**响应**:
- 成功: 返回成功消息
- 失败: 返回错误消息

#### 3.3 删除文件记录

**端点**: `/api/manage/delete/{id}`

**方法**: `POST`

**描述**: 删除文件记录（不会删除Telegram上的原始文件）

**参数**:
- `id` (必填): 文件ID

**响应**:
- 成功: 返回成功消息
- 失败: 返回错误消息

#### 3.4 编辑文件名

**端点**: `/api/manage/editName/{id}`

**方法**: `POST`

**描述**: 编辑文件的显示名称

**参数**:
- `id` (必填): 文件ID
- `fileName` (必填): 新的文件名

**响应**:
- 成功: 返回成功消息
- 失败: 返回错误消息

#### 3.5 切换点赞状态

**端点**: `/api/manage/toggleLike/{id}`

**方法**: `POST`

**描述**: 切换文件的点赞状态

**参数**:
- `id` (必填): 文件ID

**响应**:
- 成功: 返回成功消息和新的点赞状态
- 失败: 返回错误消息

#### 3.6 加入白名单

**端点**: `/api/manage/white/{id}`

**方法**: `POST`

**描述**: 将文件加入白名单，绕过内容审查

**参数**:
- `id` (必填): 文件ID

**响应**:
- 成功: 返回成功消息
- 失败: 返回错误消息

### 4. 其他 API

#### 4.1 Bing 壁纸 API

**端点**: `/api/bing/wallpaper`

**方法**: `GET`

**描述**: 获取Bing每日壁纸

**响应**:
- 成功: 返回Bing壁纸信息
- 失败: 返回错误消息

## 环境变量

项目需要以下环境变量：

| 环境变量 | 说明 |
|---------|------|
| `TG_Bot_Token` | Telegram Bot Token |
| `TG_Chat_ID` | Telegram 频道ID |
| `img_url` | Cloudflare KV 命名空间（用于文件管理） |
| `ModerateContentApiKey` | 内容审查API密钥（可选） |
| `WhiteList_Mode` | 是否开启白名单模式（可选，值为"true"或"false"） |
| `BASIC_USER` | 后台管理页面用户名（可选） |
| `BASIC_PASS` | 后台管理页面密码（可选） |

## 限制

1. 上传文件大小最大为5MB（Telegram限制）
2. Cloudflare Function 免费版每日限制100,000个请求
3. Cloudflare KV 每天有1000次免费写入额度
4. 每天最多100,000次免费读取操作
5. 每天最多1,000次免费删除操作
6. 每天最多1,000次免费列出操作

## 示例代码

### JavaScript 上传示例

```javascript
async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await fetch('/upload', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error('Upload failed');
    }
    
    const data = await response.json();
    return data[0].src;
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
}

// 使用示例
const fileInput = document.getElementById('file-input');
fileInput.addEventListener('change', async (e) => {
  const file = e.target.files[0];
  if (file) {
    try {
      const url = await uploadFile(file);
      console.log('File uploaded successfully:', url);
    } catch (error) {
      console.error('Error:', error);
    }
  }
});
```

### Python 上传示例

```python
import requests

url = 'https://your-domain.pages.dev/upload'
files = {'file': open('example.jpg', 'rb')}

response = requests.post(url, files=files)

if response.status_code == 200:
    data = response.json()
    print('File uploaded successfully:', data[0]['src'])
else:
    print('Upload failed:', response.json())
```

## 注意事项

1. 上传的文件实际存储在Telegram服务器上，项目只是提供访问链接
2. 开启内容审查后，首次加载图片会较慢，之后会缓存
3. 环境变量更改后需要重新部署才能生效
4. 超过Cloudflare免费额度后可能需要升级到付费套餐

## 常见问题

### Q: 上传失败怎么办？
A: 检查文件大小是否超过5MB，网络连接是否正常，Telegram Bot Token和Chat ID是否正确设置。

### Q: 图片无法访问怎么办？
A: 检查文件是否被加入黑名单，或者内容审查是否将其标记为不良内容。

### Q: 如何获取Telegram Bot Token和Chat ID？
A: 参考项目README.md文件中的说明。

### Q: 如何开启图片管理功能？
A: 需要在Cloudflare Pages后台设置KV命名空间绑定，并设置相应的环境变量。

## 总结

Telegraph-Image 提供了简单易用的API，支持文件上传、访问和管理。通过集成Telegram API和Cloudflare Pages，实现了免费、无限的图片存储解决方案。

如需更多帮助，请参考项目的README.md文件或GitHub仓库。