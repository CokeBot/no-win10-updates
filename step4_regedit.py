import winreg


def disable_automatic_updates() -> None:
    # 定义注册表路径
    reg_path = r"SYSTEM\CurrentControlSet\Services\UsoSvc"
    # 打开 UsoSvc 路径
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
        try:
            # 设置 Start 为4
            winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 4)

            # 查询FailureActions项并修改
            sub_key_nums, val_nums, _ = winreg.QueryInfoKey(key)
            for i in range(val_nums):
                value_name, value_data, value_type = winreg.EnumValue(key, i)

                if value_name == "FailureActions":
                    # 将二进制数据转为可变的 bytearray
                    byte_array = bytearray(value_data)
                    # 修改第3第4个字节的第5位
                    byte_array[20] = 0x00
                    byte_array[28] = 0x00
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_BINARY, bytes(byte_array))

            print("Step4: 注册表禁用Windows自动更新")
        except Exception:
            print("Step4: 注册表禁用Windows自动更新失败！")
            raise


def main():
    disable_automatic_updates()
