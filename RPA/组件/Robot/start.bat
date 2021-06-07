@rem  Copyright © Huawei Technologies Co., Ltd. 2020. All rights reserved.
@echo off

(pushd "%cd%")>nul 2>nul

(cd /d "%~dp0")>nul 2>nul

call "..\python\Robot.exe" "antrobot.pyc" %*

(popd "%cd%")>nul 2>nul

(cd /d "%cd%")>nul 2>nul