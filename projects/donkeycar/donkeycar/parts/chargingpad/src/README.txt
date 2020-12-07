
python version:2/3 

pip install flask
pip install requests

1. pi_bps 是电池管理控制服务，需要在donkey car 上面部署，配置文件都在conf.py内，启动方式
   python main.py

   后台启动
   nohop python main.py &

2. pi_cps 是充电管理服务器，需要在充电pi上安装部署，配置文件都在conf.py 启动方式

   python mian.py

   后台启动
   nohop python main.py &


待办工作：
  1. 分别在pi上部署服务
  2. 硬件上分别需要对 无线充电模块，继电器模块，LED 等进行接线和配置
  3. 需要在实机dokey car 上对电池管理单元进行电量读取
