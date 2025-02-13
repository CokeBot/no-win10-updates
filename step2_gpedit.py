import winreg


'''
修改注册表的值实现修改组策略的效果
要注意：组策略是记录历史状态的，不会读取注册表的值同步，所以组策略是看不到修改后的状态的，
    但是实际操作肯定是按注册表的值来的，所以不影响最终效果，只是无法在组策略看到改动罢了。
'''


def disable_automatic_updates() -> None:
    # 定义注册表路径
    reg_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate"
    # 打开或创建 WindowsUpdate 路径
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
        try:

            # 设置 SetDisableUXWUAccess 为1，删除扫描 Windows 更新所需的访问权限
            winreg.SetValueEx(key, "SetDisableUXWUAccess", 0, winreg.REG_DWORD, 1)

            # 尝试打开 AU 子路径，如果不存在则创建
            try:
                au_key = winreg.OpenKey(key, "AU", 0, winreg.KEY_ALL_ACCESS)
            except FileNotFoundError:
                # 如果 AU 子项不存在，创建它
                au_key = winreg.CreateKey(key, "AU")

            # 设置 NoAutoUpdate 为 1，禁用自动更新
            winreg.SetValueEx(au_key, "NoAutoUpdate", 0, winreg.REG_DWORD, 1)

            print("Step2: 组策略禁用Windows自动更新")
        except Exception:
            print("Step2: 组策略禁用Windows自动更新失败！")
            raise
        finally:
            if au_key:
                winreg.CloseKey(au_key)


def main():
    disable_automatic_updates()
