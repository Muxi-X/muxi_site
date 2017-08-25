# 木犀内网项目<img src="http://muxistudio.com/static/images/favicon/favicon-32x32.png"> 

> 我们在路上、前方不会太远


### 状态
#### 当前状态: 开发中
#### 分支

* 主分支: develop
* 开发分支: dev-branch

### 开发前准备


#### 0⃣️Git工作流

  * fork 项目仓库

    > 在github上fork这个仓库

  *  clone fork的项目仓库
    
    ```
    $ git clone https://github.com/<your_username>/muxi_site.git
    ```

  * 从develop分支开出功能分支(以feature为例)
  **注意⚠️  : develop分支为主分支！！！**
  
  ```
  git checkout develop
  git checkout -b <feature>
  ```
  
  * 在feature分支进行功能开发
  
  ```
  写写写写写..............代码
  ```
  * 本地调试
  
  ```
  确保代码修改可以在本地调试通过
  ```
  
  * 向feature分支提交

  ```
  请提交时只提交改动的文件，并写好commit信息
  ```
  * 在Github 上向develop分支发送pull request
 
  ```
  创建PR之前仔细检查更改的文件！
  ```
  
  * merge，发布版本，进行部署(项目维护人负责)
  
  ```
  merge 之前仔细检查更改的文件！
  ```

#### 1⃣️本地环境搭建
1.安装Flask

* 教程: [Flask](http://docs.jinkan.org/docs/flask/installation.html#installation)

2.安装扩展环境

  * 进入虚拟环境(还是请参见教程)

  ```
  $ pip install -r requirment.txt
  ```

  * 下载速度较慢时的解决方案：

    * 切换为豆瓣源：
   
       ```
       pip install --index-url http://pypi.doubanio.com/simple/ -r requirements.txt --trusted-host=pypi.doubanio.com
       ```
    * 终端代理(proxychains + shadowsocks):
    [ProxyChains-NG](https://github.com/rofl0r/proxychains-ng)

3.设置测试域名

* 打开hosts文件

   ```
   $ sudo vim /etc/hosts
   ```

* 设置测试域名,在文件后面添加
    
    ```
    127.0.0.1 blog.flask.dev
    127.0.0.1 share.flask.dev
    127.0.0.1 book.flask.dev
    127.0.0.1 auth.flask.dev
    127.0.0.1 profile.flask.dev
    127.0.0.1 i.flask.dev
    ```
    
4.设置环境变量

  * 打开.bashrc(或.zshrc)

    ```
    $ vim ~/.bashrc(~/.zshrc)
    ```
  * 设置环境变量,在文件后添加

    ```
    set MUXI_WEBSITE_SERVERNAME
    export MUXI_WEBSITE_SERVERNAME="flask.dev:5000"
    ```
  * 重新加载配置文件

    ```
    $ source ~/.bashrc(~/.zshrc) 
    ```
  
5.构建本地测试数据库
   
  * 初始化
   
    ```
    $ python manage.py db init
    ```

  * 数据库已存在

    ``` 
    $ python manage.py db migrate; python manage.py db upgrade
    ```

6.创建用户角色
  
  ```
  $ python manage.py insert_roles
  ```

7.运行项目测试

  ```
  python manage.py runserver
  ```
  * 当前路由:
  
  ```
  i.flask.dev:5000/  木犀官网
  book.flask.dev:5000/ 木犀图书
  share.flask.dev:5000/ 木犀分享
  blog.flask.dev:5000/ 木犀博客
  profile.flask.dev:5000/<int: id>/ 木犀个人页
  ```
  确定每个页面都没有问题之后就可以开始开发了。🐳

#### 2⃣️开发完成之后


1. Docker测试
   
  * 编写 muxiwebsite.env
  
    ```
    MUXI_WEBSITE_SQL=mysql://<username>:<password>@<url-to-rds>/<database-name>
    MUXI_WEBSITE_SERVERNAME=muxixyz.com
    ZAODU_URL=""    
    ```

  * 运行
  
    ```
    $ docker-compose build;docker-compose up
    ```

2. 提交到Github，等待管理员merge⌛️

3. 根据情况修改 muxiwebsite.env并上传到部署服务器

   ```
   scp /url/to/muxiwebsite.env <username>@<host>:/url/to/destination/directory
   ```
4. 等待管理员部署⌛️

### ToDo

- [ ] RESTful API

### 进度

    2015年10月19号: 木犀图书测试版1.0上线，1.0+正在修bug
    -----------------------------------------------------
    2015年10月19日: 木犀分享完成基本功能，下一步整合markdown编辑器和优化
    -----------------------------------------------------
    2015年10月20日: 木犀分享完成分页功能、权限管理
    -----------------------------------------------------
    2015年10月22日: 总结此仓库的合作方式(前后端)，因为有点混乱有点烦
    -----------------------------------------------------
    2015年10月23日: 完成博客数据库model编写, master<->development
    -----------------------------------------------------
    2015年11月5日 : 木犀分享基本功能完成，待前端修改相关样式
    -----------------------------------------------------
    2015年11月7日 : 编写data脚本，自动构建本地测试数据库
    -----------------------------------------------------
    2015年11月9日 : 新的开发分支 develop 替代 development
    -----------------------------------------------------
    2015年11月16日: 编写统一后台管理界面
    -----------------------------------------------------
    2015年11月18日: 完成统一后台管理
    -----------------------------------------------------
    2015年11月20日: 完成木犀分享hot板块(排序)
    -----------------------------------------------------
    2015年12月15日: 整合木犀博客(基本完成)
    -----------------------------------------------------
    2015年12月24日: 完成木犀博客的归档，添加profile个人页
    -----------------------------------------------------
    2016年1月13日: ISSUE 认领, 最后清扫工作开始
    -----------------------------------------------------
    2016年1月15日: 编写官网分享API: 木犀内外开始😄
    -----------------------------------------------------
    2016年1月17日: 完成木犀内外API, close掉了一系列的ISSUE
    -----------------------------------------------------
    2016年2月1日: 集成木犀个人信息修改页
    ----------------------------------------------------
    2016年5月25日：设置子域名,新的主分支develop代替master,开发分支dev-branch代替develop
    ----------------------------------------------------
    2016年7月7日: 木犀分享、图书、个人页更新完成
    ----------------------------------------------------
    2016年11月1日: Docker部署
