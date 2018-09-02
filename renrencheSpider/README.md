### 爬取人人车的所有二手车信息



>   auth: zhangminglu
>
>   datetime: 2018-03-16 20:45
>
>   Email: 1367000465@qq.com
>
>   Github: https://github.com/zhangMingLu
>
>   CSDN: https://blog.csdn.net/zhang_ming_lu



### 爬虫项目结构介绍

-   [基础版(renrencheSpider)](renrencheSpider/)： 未使用分布式, 用时8个小时爬取20万条数据, 查看[README文件](renrencheSpider/README)
-   [分布式版(renrenche_fengbushi)](renrenche_fengbushi/)： 使用分布式，实现多个 slave 快速稳定爬取数据(详细介绍，分布式版本的[README](renrenche_fengbushi/README)文件）
    -   master采用 urllib+lxml+scapy实现快速写入url到消息队列, 同时优化slave实现协助master进行快速解析(未完成最后的优化, 将master在任务完成后自动变为slave,执行slave的任务)

### 展示页面



#### [Django框架展示数据(RRC_show_by_Django)](RRC_show_by_Django/)

-   可以显示基本的数据， 更多功能有空闲再添加

#### [Flask框架展示数据（RRC_show_by_Flask）](RRC_show_by_Flask/)

-   页面显示出现问题，未解决， 有空闲会一一解决。



-   同时也将Flask开始项目时需要的一些最基本的配置做了简单的模块化，可以参考这里[快速开始进行Flask项目](https://github.com/zhangMingLu/A_demo_for_easy_start_flask_project)

