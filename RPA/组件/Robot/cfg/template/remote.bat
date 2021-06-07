@rem  Copyright © Huawei Technologies Co., Ltd. 2020. All rights reserved.
@echo off
for /f "skip=1 tokens=3" %%s in ('query user %USERNAME%') do (
  %windir%\System32\tscon.exe %%s /dest:console
)