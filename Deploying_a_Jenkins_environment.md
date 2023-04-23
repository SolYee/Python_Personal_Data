##CentOS 7 部署 Jenkins 持续集成环境
Jenkins是一种流行的开源 CI（持续集成）工具，广泛用于项目开发，部署和自动化。

本文将引导你完成在 CentOS 7 服务器实例上安装 Jenkins 的过程。

1. 先决条件
之前，你必须具备：
        从零开始部署了 CentOS 7 服务器实例。
        root 权限
2. 部署阿里云源



```powershell
curl -o /etc/yum.repos.d/CentOS-Base-ali.repo http://mirrors.aliyun.com/repo/Centos-7.repo

curl -o /etc/yum.repos.d/epel-7-ali.repo http://mirrors.aliyun.com/repo/epel-7.repo

yum clean all

yum makecache
```


3. 安装 Java
	
在安装 Jenkins 之前，需要在系统上安装一个 Java 虚拟机。在这里，让我们使用 yum 安装最新的 JDK：

```powershell
yum install -y java
```

安装完成后，可以通过运行以下命令进行确认：

```powershell
java -version
```


4. 安装 Jenkins

```powershell
curl -o /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat-stable/jenkins.repo

rpm --import http://pkg.jenkins-ci.org/redhat-stable/jenkins-ci.org.key
```


使用官方的 yum 安装最新的稳定版本的 Jenkins：

```powershell
yum install -y jenkins
```

启动 Jenkins 服务并将其设置为在启动时运行：

```powershell
systemctl start jenkins.service

systemctl enable jenkins.service
```

为了允许访问者访问 Jenkins，你需要允许端口 8080 上的入站流量：

```powershell
firewall-cmd --zone=public --permanent --add-port=8080/tcp

firewall-cmd --reload
```

现在，通过从浏览器访问以下地址来访问 Jenkins：

```powershell
http://服务器IP:8080
```

4.1. 基本配置

解锁 jenkins

根据提示使用 cat 命令查看密码

```powershell
cat /var/lib/jenkins/secrets/initialAdminPassword
```

自定义 Jenkins

	Jenkins 插件自动从网络下载安装，由于插件服务器在国外，会产生网络延迟问题导致安装失败。
	
	因此选择选择插件来安装。本次我们将不选择任何插件以快速安装，后期将通过插件管理器安装所需插件。
	
	创建第一个管理员用户

	实例配置
	
	可修改 地址与端口，不建议修改。保持默认。
	
    插件安装
	
	系统管理Manage Jenkins -> 管理插件Manage Plugins -> 可选插件Available -> 过滤filter



> `HTML Publisher`

> `Workspace Cleanup`

> `Subversion`

> `Startup Trigger`

> `Groovy`

> `Email Extension`

5. 部署 Python 3
	部署编译环境

```powershell
yum -y groupinstall 'Development Tools'

yum -y install zlib zlib-devel libffi-devel openssl-devel
```

Python 官网下载最新版 Python 源代码。
	
本文以 Python-3.8.5 为例

```powershell
cd /tmp

curl -O https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz

tar -xf Python-3.8.5.tgz
```

Python 配置

```powershell
./Python-3.8.5/configure
```

构建并安装 Python 3

```powershell
make -j install Python-3.8.5
```

确认 Python 3 部署成功

```powershell
python3 --version
```

安装自动化依赖 Python 相关库

```powershell
pip3 install selenium htmlreport -i https://mirrors.aliyun.com/pypi/simple/

pip3 list
```

6. Jenkins 相关

配置文件 `/etc/sysconfig/jenkins`

默认启用 `8080`

日志 `/var/log/jenkins/jenkins.log`

服务状态 `systemctl status jenkins`

启动服务 `systemctl start jenkins`

停止服务 `systemctl stop jenkins`

重启服务 `systemctl restart jenkins`

