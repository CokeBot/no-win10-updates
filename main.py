import os
import step1_services as step1
import step2_gpedit as step2
import step3_taskschd as step3
import step4_regedit as step4

step1.main()
step2.main()
step3.main()
step4.main()
# 保持窗口不关闭
os.system("pause")      # 方法 2：适用于 Windows 系统
