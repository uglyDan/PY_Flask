# Flask API 服务

这是一个结构化的Flask API服务，提供图片上传及描述、故事列表和播放等功能。

## 项目结构

```
/
├── app/                          # 应用主目录
│   ├── __init__.py              # 应用初始化
│   ├── config/                  # 配置目录
│   │   └── config.py            # 配置文件
│   ├── routes/                  # 路由目录
│   │   ├── api.py               # API路由
│   │   └── upload.py            # 上传路由
│   ├── services/                # 服务目录
│   │   └── image_service.py     # 图像服务
│   ├── static/                  # 静态文件
│   ├── templates/               # 模板文件
│   └── utils/                   # 工具函数
│       └── file_utils.py        # 文件工具
├── uploads/                     # 上传文件存储目录
├── mp3/                         # 音频文件存储目录
├── api_data.json                # API数据
├── api_list.json                # API列表
├── api_story.json               # 故事数据
├── requirements.txt             # 项目依赖
├── run.py                       # 启动脚本
└── README.md                    # 说明文档
```

## 安装和运行

1. 安装依赖:
```
pip install -r requirements.txt
```

2. 运行应用:
```
python run.py
```

应用将在 `http://0.0.0.0:5000` 启动。

## API 接口

### 图片上传
- URL: `/api/upload_image`
- 方法: `POST`
- 功能: 上传图片并获取AI生成的图片描述

### 获取API列表
- URL: `/api/list`
- 方法: `GET`
- 功能: 获取API列表数据

### 获取首页数据
- URL: `/api/data`
- 方法: `GET`
- 功能: 获取首页数据

### 获取故事列表
- URL: `/api/story?jump_value={id}`
- 方法: `GET`
- 功能: 根据故事类型获取故事列表

### 获取故事播放信息
- URL: `/api/story_url?id={id}`
- 方法: `GET`
- 功能: 获取故事播放信息

### 获取故事媒体文件
- URL: `/api/story_url_media/{filename}`
- 方法: `GET`
- 功能: 获取故事媒体音频流 