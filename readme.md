<h1>paimon短链接</h1>

<p1>基于flask和redis的短链接生成器</p1>

## 预览
<img src="https://img.alistnas.top/file/55f390daa9fe9fdf160cf.png"></img>

## 项目结构
```
├─.idea  # pycharm配置文件
│  ├─dataSources
│  └─inspectionProfiles
├─models  # 项目模型
├─static  # 项目静态文件
|─templates  # 项目模板
```
## 部署方法
### 1.克隆到本地
```bash
git clone https://github.com/ischenyu/short_link.git
```
### 2.安装依赖
```bash
cd short_link
pip install -r requirements.txt
```
### 3.编辑配置文件
配置文件位于项目目录下的config.yaml中
```yaml
server:  # 服务器配置
    host: 0.0.0.0  # 服务器地址
    port: 5001  # 端口
    debug: False  # 是否开启debug模式

redis:  # redis配置
    host: 127.0.0.1  # redis地址
    port: 6379  # redis端口
    password: Dingtalk124561017  # redis密码
    db: 0  # redis数据库
```

### 4.启动服务
```bash
python app.py
```
