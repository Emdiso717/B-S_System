# 商品比价系统——Price Sleuth

本项目基于Docker的前后端分离商品比价系统，使用Django + Vue.js + MySQL技术栈实现。

## 1 环境要求

- Docker
- Docker Compose
- 相关镜像请确保一下镜像以及拉取，如果没有请手动拉取：
```bash
docker pull python:3.11
docker pull node:16
docker pull nginx
```

## 2 快速启动

1. 克隆项目或者直接下载压缩包

```bash
git clone https://github.com/Emdiso717/B-S_System.git
```

2. 启动服务
```bash
docker-compose up -d
```

3. 访问服务
- 前端界面: http://localhost:8080
- 后端API: http://localhost:8000

## 3 操作与测试

详细信息请见 `doc/用户使用手册.pdf` ,在这里简单介绍流程：

- 用户注册
- 用户登录
- 搜索收藏比价商品，查看用户信息
- 管理员登录：
  - 账号 ：superqjz
  - 密码：12345678
- 查询所有商品价格、发降价邮件

## 4 服务配置

| 服务   | 端口 | 说明                  |
| ------ | ---- | --------------------- |
| Vue    | 8080 | 前端服务              |
| Django | 8000 | 后端API服务           |
| MySQL  | 3307 | 数据库 (外部访问端口) |

## 5 数据库配置

- 数据库名：commodity_system
- 端口：3307
- 用户名：root
- 密码：123717
