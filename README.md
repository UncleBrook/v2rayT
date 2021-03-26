# v2rayT

终端环境下订阅 `v2ray` 或者 `xray` 服务脚本

## 使用
可以将本脚本添加到  `/usr/bin` 或 `/usr/sbin` 或 `/bin`，或参考 `echo $PATH` 下的具体位置
或者使用下面命令
```
$ sudo su
$ curl https://raw.githubusercontent.com/UncleBrook/v2rayT/master/v2t > /usr/sbin/v2t && chmod a+x /usr/sbin/v2t
```

v2ray 安装过程请参考 [v2ray](https://github.com/v2fly/fhs-install-v2ray/blob/master/README.zh-Hans-CN.md)
```
$ bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)
```

Xray 安装过程请参考 [Xray](https://github.com/XTLS/Xray-install)
```
$ bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```
