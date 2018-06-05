<h3>本项目为使用python分析电动汽车电池数据</h3>
数据是120辆电动汽车(出租车)在2015年4月16日一天的运行中，由电池传感器传出，格式为xls，约600Mb。
<br>
使用jupyter notebook作为主要工具，代码存于ipy_notebook_workplace/目录下
<br>
<h4>主要内容：</h4>
batteryString用于分析电池组每个电池的电压分布，找出与其他电池电压一致性较差的电池并绘图；
<br>
correlationAnalysis用于分析单个电池组中电流、电压、剩余电量、当日行驶里程两两之间的关系并绘图；
<br>
correlationAnalysisAll用于分析全部电池组中电流、电压、剩余电量、当日行驶里程两两之间的关系并绘图；
<br>
tmperatureField用于分析温度域，分析单个电池组中温度标准差，温度分布，电压标准差，电压分布两两之间的关系并绘图；
<br>
functionGroup收录ETL常用函数。
<br>

<h4>其他内容：</h4>
scatter绘制全部电池组中电流与电压的散点图；
<br>
energyCost计算单个及全部电池组的一日能耗；
<br>
averageVariance计算单个电池组电流均方差和极差；
<br>
maxTemperature找出每个电池组的温度最大值；
<br>
driveBehavior根据坐标绘制当日分时行驶路径；
<br>
stopTime找出停车超过10分钟的时间段。

