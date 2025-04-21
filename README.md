# JX3 QQ Bot （剑网3查询机器人）

基于 [botpy](https://github.com/tencent-connect/botpy) + [JX3API](https://www.jx3api.com) 构建的 QQ 官方机器人。支持通过频道私信快速查询剑网3信息。

---

## 功能支持

- 开服状态查询
- 活动日历查询
- 角色查询：名片、装备、副本cd、资历、奇遇
- 物价查询
- 团队招募
- 一之窟解密

---

## 快速部署方式（本地 / 云服务器）

### 克隆代码
```bash
git clone https://github.com/Kaibo-He/JX3QQbot.git
cd JX3QQbot
```
### 安装依赖
```bash
pip install -r requirements.txt
```

### 设置环境变量
```bash
cp .env.template .env
nano .env
```
并填写你的机器人凭据
```bash
BOT_APPID=你的 AppID
BOT_SECRET=你的 Secret
BOT_TOKEN=你的 Token
```

### 启功机器人
```bash 
python main.py 
```

