近日，“何同学”团队盗用Github用户“vietnh1009”的开源项目《ASCII-generator》，引起广泛争议。本人是一名编程爱好者，多多少少具备Python、C、C++、Rust、Haskell等编程语言的使用经验，编程水平比较充分，因此想要通过重构该项目（[重构项目链接](https://github.com/Wangsutan/ASCII-generator-master)），深入学习相关技术并提高编程水平。本次重构大幅提高了代码质量，也方便感兴趣的朋友从中体验字符画技术的一些基本原理。现在将我在重构中的一些经验和体会分享给大家。

---

## 一、下载方式问题

我首先尝试用`git clone https://github.com/vietnh1009/ASCII-generator.git`的方式，克隆Github上的该项目。但是下载过程显得比较吃力，长时间卡在大约一半的进度上。在长时间等待无果的情况下，我使用了直接下载`.zip`压缩包的方式。经过检查，发现压缩包中图片和视频等素材和生成结果占用空间最多。下面展示了压缩包的大小和解压缩后的项目文件大小。

```
stat ASCII-generator-master.zip
  文件：ASCII-generator-master.zip
  大小：558375439       块：1090592    IO 块大小：4096   普通文件
设备：8,2       Inode: 4721313     硬链接：1
权限：(0644/-rw-r--r--)  Uid: ( 1000/     wst)   Gid: ( 1000/     wst)
访问时间：2024-11-21 09:00:50.000000000 +0800
修改时间：2024-11-20 23:42:11.000000000 +0800
变更时间：2024-11-23 22:54:13.435682087 +0800
创建时间：2024-11-21 09:00:34.984010443 +0800
```

```
ncdu 2.5 ~ Use the arrow keys to navigate, press ? for help
--- /home/wst/Desktop/test/ASCII-generator-master -----------------------------------------------------
                             /..
  501.2 MiB [##############] /demo
   37.9 MiB [#             ] /fonts
   24.6 MiB [              ] /data
    8.0 KiB [              ]  utils.py
    4.0 KiB [              ]  video2video_color.py
    4.0 KiB [              ]  video2video.py
    4.0 KiB [              ]  README.md
    4.0 KiB [              ]  img2img_color.py
    4.0 KiB [              ]  img2img.py
    4.0 KiB [              ]  img2txt.py
    4.0 KiB [              ]  alphabets.py
    4.0 KiB [              ]  LICENSE

*Total disk usage: 563.8 MiB   Apparent size: 563.7 MiB   Items: 46
```

一些专业的程序员嘲讽“何同学”团队以及何世杰本人不会用`git`，在技术方面确实有一定道理，但也具有一些情绪化的成分。如果读者想要快速体验相关代码，甚至可以考虑直接在网页上，把该项目的7个代码文件直接复制下来，这样可能还更快一些。

## 二、项目结构

该项目是一个关于字符画的小项目，Python代码行数只有约500行。经过本人的摸索和体验，该项目中的文件的基本结构是这样的：

- `data`文件夹存放测试用的图片和视频，相关脚本的命令行默认参数会包括这些素材。
- `demo`文件夹存放的是各种输出示例。它的大小高达501.2Mib。
- `fonts`文件夹存放一些字体，这些字体用于在图片或视频上生成字符图形。
- 7个Python脚本文件，其中，`alphabets.py`用于存放所需字符，`utils.py`是一个核心部件，其中的两个函数用于读取和排序`alphabets.py`中的字符。其他的脚本用于处理不同的字符画业务。
- `LICENSE`文件是一个关于软件许可证的文件，其中写明了MIT协议，这是一种极为宽松的协议。何同学团队违背该协议要求，删掉了原作者重要信息，声称是自己写的。
- `README.md`文件包含对该项目的简单介绍。

## 三、代码的质量与重构

通过阅读和调试该软件，发现该软件存在一些重要的缺点：

- 存在大量重复代码。
- 核心逻辑虽然是正确的，但是功能杂糅在一起，几乎无法正常阅读。
- `getsize`等写法目前已经过时，许多代码已无法在主流软件版本下正常执行。
- 没有类型注解。
- 异常处理不到位。

本人根据自己的认识和体会，对该项目进行了一次彻底的重构，重点包括以下方面：

- 将与字符相关的核心数据统一放到`alphabets.py`模块中，而不再分散到业务代码中。
- 将读取命令行参数的函数与具体的业务代码解耦，直接向业务相关函数传递明确的参数，而不再传递模糊的`argparse.Namespace`类型的参数。
- 将字符画核心算法进行拆分和重组，做成若干函数，放到`utils.py`模块中。函数名和变量名具有比较充分的意义，大幅提高了代码的自解释性。在过程中，还发现了一个隐晦的逻辑错误，就是一处`scale`缩放值被错误地写成了一个固定的字面量。
- 添加了充分的类型注解。
- 优化了异常处理。

通过`black`、`mypy`、`flake8`等命令，检查和优化该代码。相关运行结果如下：

```
(base) [wst@wst-h310ms220 ASCII-generator-master]$ black *.py
All done! ✨ 🍰 ✨
7 files left unchanged.
(base) [wst@wst-h310ms220 ASCII-generator-master]$ mypy *.py
Success: no issues found in 7 source files
(base) [wst@wst-h310ms220 ASCII-generator-master]$ flake8 --max-line-length=125
```

重构之后的代码，仍然存在一些重复代码。但代码逻辑已经非常清晰，后续如果需要进一步优化，也会非常方便。

---

总的来说，本人对该项目的重构，大幅提高了代码的质量和可维护性，也加深了我对字符画技术的理解。大家如果赏光阅读我重构的代码，应该也会有所收获。
