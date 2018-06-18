使用说明：
1.在main中放入测试字符串，就获取返回结果,例如res=ter.main('我这周日还可以么，也就是这个星期六，我尽量在下周一就把还了,不不我还是后天还得了,我30号还,17号,下个月15号,你厉害7月15号就还，我哈恩好7月18日')
2.运行time_regx_recognize.py文件即可

在time_regx_recognize.py文件中：
1.凡是词汇在self.week_to_sequence、self.num_to_sequence、self.num_next_to_sequence出现过的都可以测试
2.凡是出现XX月XX日的都可以测试：例如我9月18号就还