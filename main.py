import psutil
from datetime import datetime
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register


@register("astrbot_plugin_sysinfo", "mika", "获取当前系统状态", "1.0.0", "https://github.com/AstrBot-Devs/astrbot_plugin_sysinfo")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("sysinfo")
    async def sysinfo(self, event: AstrMessageEvent):
        '''获取系统信息'''
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        net_info = psutil.net_io_counters()
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        process_count = len(psutil.pids())
        net_connections = len(psutil.net_connections())

        sys_info = (
            f"系统信息:\n"
            f"CPU 使用率: {cpu_usage}%\n"
            f"CPU 核心数: {cpu_count}\n"
            f"内存总量: {memory_info.total / (1024 ** 3):.2f} GB\n"
            f"内存使用: {memory_info.percent}%\n"
            f"磁盘总量: {disk_info.total / (1024 ** 3):.2f} GB\n"
            f"磁盘使用: {disk_info.percent}%\n"
            f"网络发送: {net_info.bytes_sent / (1024 ** 2):.2f} MB\n"
            f"网络接收: {net_info.bytes_recv / (1024 ** 2):.2f} MB\n"
            f"系统启动时间: {boot_time}\n"
            f"当前运行进程数: {process_count}\n"
            f"当前网络连接数: {net_connections}"
        )
        
        yield event.plain_result(sys_info)
