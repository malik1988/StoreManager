# StoreManager
store manager in python

## 说明
通过串口通讯接收消息并显示


## 技术
- 数据库sqlite
- python3


## 程序打包
- 支持打包工具pyinstaller 
由于最新版pyinstaller-3.2.1只支持<=python3.5，python3.6会出现"IndexError: tuple index out of range"，因此推荐使用python3.5.
- 打包方法：
```
pyinstaller main.spec
```


