import win32serviceutil
import win32service
import win32con

# Windows Update 服务名称
service_name = "wuauserv"


def disable_service_start_type() -> None:
    try:
        # 修改服务的启动类型为禁用 (SERVICE_DISABLED)
        win32serviceutil.ChangeServiceConfig(
            None,  # 服务器名称，None表示本地计算机
            service_name,
            startType=win32con.SERVICE_DISABLED
        )
        print(f"Step1: 服务 '{service_name}' 启动类型已设置为禁用")
    except Exception:
        print(f"Step1: 服务 '{service_name}' 启动类型设置失败！")
        raise


def set_service_recovery_no_operation() -> None:
    # 获取服务控制管理器句柄
    scm_handle = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
    # 获取服务句柄
    service_handle = win32service.OpenService(scm_handle, service_name, win32service.SERVICE_ALL_ACCESS)
    try:
        new_recovery_options = {
            'ResetPeriod': 864000000,  # 重置计数器的时间间隔，单位为秒，86400(24h) * 10000 = 1w天 = 27年
            'RebootMsg': None,  # 重启时显示的消息，未设置
            'Command': None,  # 失败时执行的命令，未设置
            'Actions': ((0, 0), (0, 0), (0, 0))  # 三次失败均无操作
        }

        # 设置服务的失败恢复操作
        win32service.ChangeServiceConfig2(service_handle, win32service.SERVICE_CONFIG_FAILURE_ACTIONS,
                                          new_recovery_options)

        # 查询服务的配置，包括恢复操作
        recovery_options = win32service.QueryServiceConfig2(
            service_handle,
            win32service.SERVICE_CONFIG_FAILURE_ACTIONS
        )
        print(f"Step1: 服务 '{service_name}' 恢复选项参数设置为 {recovery_options} ")
    except Exception:
        print(f"Step1: 服务 '{service_name}' 恢复选项参数设置失败！")
        raise
    finally:
        # 关闭服务句柄
        win32service.CloseServiceHandle(service_handle)
        # 关闭服务管理器句柄
        win32service.CloseServiceHandle(scm_handle)


def main():
    disable_service_start_type()
    set_service_recovery_no_operation()
