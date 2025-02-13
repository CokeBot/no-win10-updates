import win32com.client


def del_all_windows_update_task() -> None:
    try:
        # 连接到任务计划程序服务
        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()

        # 获取任务计划程序的根文件夹
        rootFolder = scheduler.GetFolder('\\Microsoft\\Windows\\WindowsUpdate')

        # 删除计划程序中windows更新的所有任务
        for task in rootFolder.GetTasks(0):
            # 第二个参数 0 表示如果任务不存在则不会抛出异常。
            rootFolder.DeleteTask(task.Name, 0)

        print("Step3: 任务计划程序删除所有相关window更新任务")
    except Exception:
        print("Step3: 任务计划程序删除所有相关window更新任务失败！")
        raise


def main():
    del_all_windows_update_task()
