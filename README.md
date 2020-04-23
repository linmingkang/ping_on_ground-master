1. 进入mysql数据库，查看是否有train_connectivity、train_ip、train_online_flag这三张数据表，没有则导入：  
　　use db_ground_transfer;  
　　source 该文件夹的绝对路径/train_connectivity.sql  
　　source 该文件夹的绝对路径/train_ip.sql  
　　source 该文件夹的绝对路径/train_online_flag.sql  

2. 务必导入以上三张数据表，否则程序不起作用  

3. 确保配置文件'/home/chsr/cf.d/groundusr.conf'存在  

4. 安装pymysql库：  
    tar xvf PyMySQL-0.9.3.tar.gz  
    cd PyMySQL-0.9.3  
    python3 setup.py install  

5. 编译看门狗程序：  
    g++ daemon_ping_on_ground.cpp -o daemon_ping_on_ground  
    cp daemon_ping_on_ground /home/chsr/bin/  

6. 若未创建看门狗日志目录，则创建：  
    mkidr -p /home/chsr/log.d  
    
7. 运行程序：  
    cp ping_on_ground.py /home/chsr/bin/  
    /home/chsr/bin/daemon_ping_on_ground
