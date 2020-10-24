Pre install steps
===

## install pyBuilder
pyBuilder helps to build python project

```
pip3 install pyb
pyb
```

## external packages
### Ffmpeg installation:
``` 
    sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-$(rpm -E '%{rhel}').noarch.rpm
    
    sudo yum install epel-release
    
    sudo yum localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
    
    sudo yum install ffmpeg ffmpeg-devel
```
