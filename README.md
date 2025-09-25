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

> 该项目只适合在软路由环境使用，不推荐在日常机使用（毕竟你可能玩着游戏结果发现自己的鼠标卡住了）
>
> 如果要在自己的日常机使用，目前也正在开发相关的GUI，敬请期待

可以自动模拟点击完成登录，并自动检测是否在线，不在线的情况下会自动重新登录（部分学校48小时后会强制性下线），适合在ESXi等虚拟机构造共享网络

针对官方客户端臃肿的特点，创新使用PsSuspend对UI线程进行挂起处理，在不影响正常上网的前提下大大减少CPU占用率，对软路由等受限环境非常友好

## 使用

1. 前往[Release](https://github.com/250king/ESurfingAutoLogin/releases)下载最新版

2. 在官方客户端设置好账号密码并设置记住密码

3. （选做但推荐）下载[PsSuspend](https://learn.microsoft.com/zh-cn/sysinternals/downloads/pssuspend)并将其中的
   ```pssuspend64.exe```放在```C:/Windows/System32```之下，或者给文件所在位置加入PATH变量

   如果是32位系统，请不要下载带有***64***结尾的可执行文件

4. 进入控制面板→管理工具→计算机管理→任务计划程序，新建开机任务，并***赋予最高运行权限***

如果需要解冻客户端，在程序运行界面直接```Ctrl+C```中止程序即可，会自动帮忙解冻程序

## 环境变量配置

| 参数名                 | 说明                                                                                   |
|---------------------|--------------------------------------------------------------------------------------|
| ESURFING_TIMEOUT    | 检测超时时间，单位秒，默认10秒                                                                     |
| ESURFING_RETRY      | 重试次数，默认3次                                                                            |
| ESURFING_INTERVAL   | 检测间隔时间，单位秒，默认30秒                                                                     |
| ESURFING_SERVER     | 检测服务器，默认阿里云DoH                                                                       |
| ESURFING_EXECUTABLE | 官方客户端可执行文件路径，默认```C:/Program Files (x86)/Chinatelecom_GDPortal/EsurfingClient.exe``` |

## 构造

项目基于Python编写，一方面可以直接使用Python运行环境直接使用，另一方面可以使用Nuitka等打包工具来打包成二进制可执行文件，在这里以Nuitka为例

请注意，由于最后一个支持Windows 7的Python版本是3.8，因此推荐使用Python3.8进行构建。如果Windows版本更高，可以直接使用最新版。推荐使用Tiny版本的Windows

使用Nuitka之前需要安装[Microsoft C++生成工具](https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/)

先安装好相应的依赖

```pip install nuitka httpx pywin32 loguru```

安装后开始打包编译

```nuitka --onefile --windows-uac-admin --output-dir=./build main.py```

编译成功后可以在```build```目录看到```main.exe```