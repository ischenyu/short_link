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
配置文件位于项目目录下的config.py中


### 4.启动服务
```bash
python app.py
```
