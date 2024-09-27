# ESurfingAutoLogin
[![GitHub License](https://img.shields.io/github/license/250king/ESurfingAutoLogin?style=flat-square)](https://github.com/250king/ESurfingAutoLogin/blob/main/LICENSE)

广东天翼校园客户端自动登录器
> 为保障项目安全，请不要随意在各个社交平台广泛传播该项目，包括不限于Bilibili、QQ、X（Twitter）、Discord
> 
> 个人兴趣而制作，开发目的在于学习和探索，一切开发皆在学习，请勿用于非法用途
> 
> 因使用本项目产生的一切问题与后果由使用者自行承担，项目开发者不承担任何责任
> 
> 因项目特殊性，随时会删档

## 功能
可以自动模拟点击完成登录，并自动检测是否在线，不在线的情况下会自动重新登录（部分学校48小时后会强制性下线），适合在ESXi等虚拟机构造共享网络

针对官方客户端臃肿的特点，创新使用PsSuspend对UI线程进行挂起处理，在不影响正常上网的前提下大大减少CPU占用率，对软路由等受限环境非常友好

## 使用
1. 前往[Release](https://github.com/250king/ESurfingAutoLogin/releases)下载最新版

2. 在官方客户端设置好账号密码并设置记住密码

3. 下载[PsSuspend](https://learn.microsoft.com/zh-cn/sysinternals/downloads/pssuspend)并将其中的```pssuspend64.exe```放在```C:/Windows/System32```之下，或者给文件所在位置加入PATH变量（选做但推荐）

4. 进入控制面板→管理工具→计算机管理→任务计划程序，新建开机任务，并***赋予最高运行权限***

## 构造
项目基于Python编写，一方面可以直接使用Python运行环境直接使用，另一方面可以使用Nuitka等打包工具来打包成二进制可执行文件，在这里以Nuitka为例

请注意，由于最后一个支持Windows 7的Python版本是3.8，因此推荐使用Python3.8进行构建。如果Windows版本更高，可以直接使用最新版

使用Nuitka之前需要安装[Microsoft C++生成工具](https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/)

先安装好相应的依赖

```pip install nuitka httpx pywin32 loguru```

安装后开始打包编译

```nuitka --onefile --windows-uac-admin --output-dir=./build main.py```

编译成功后可以在```build```目录看到```main.exe```