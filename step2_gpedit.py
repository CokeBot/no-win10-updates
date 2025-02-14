import winreg

'''
修改注册表的值实现修改组策略的效果
要注意：组策略是记录历史状态的，不会读取注册表的值同步，所以组策略是看不到修改后的状态的，
    但是实际操作肯定是按注册表的值来的，所以不影响最终效果，只是无法在组策略看到改动罢了。
'''


def disable_automatic_updates() -> None:
    # 定义注册表路径
    reg_path = r"SOFTWARE\Policies\Microsoft\Windows"
    # 打开或创建 WindowsUpdate 路径
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
        try:
            # 尝试打开 WindowsUpdate 子路径，如果不存在则创建
            wu_key = create_key_if_not_exist(key, "WindowsUpdate")
            # 设置 SetDisableUXWUAccess 为1，删除扫描 Windows 更新所需的访问权限
            winreg.SetValueEx(wu_key, "SetDisableUXWUAccess", 0, winreg.REG_DWORD, 1)

            # 尝试打开 AU 子路径，如果不存在则创建
            au_key = create_key_if_not_exist(wu_key, "AU")
            # 设置 NoAutoUpdate 为 1，禁用自动更新
            winreg.SetValueEx(au_key, "NoAutoUpdate", 0, winreg.REG_DWORD, 1)

            print("Step2: 组策略禁用Windows自动更新")
        except Exception:
            print("Step2: 组策略禁用Windows自动更新失败！")
            raise
        finally:
            if au_key:
                winreg.CloseKey(au_key)
            if wu_key:
                winreg.CloseKey(wu_key)


def create_key_if_not_exist(
        key: winreg.HKEYType,
        sub_key_name: str
) -> winreg.HKEYType:
    # 尝试打开 sub_key 子路径，如果不存在则创建
    try:
        sub_key = winreg.OpenKey(key, sub_key_name, 0, winreg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        # 如果 sub_key 子项不存在，创建它
        sub_key = winreg.CreateKey(key, sub_key_name)
    return sub_key


def main():
    disable_automatic_updates()
