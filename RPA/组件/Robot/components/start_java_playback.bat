@rem  Copyright © Huawei Technologies Co., Ltd. 2020. All rights reserved.
@rem **********************************************************************
@rem * Script to start java playbacker *
@rem * Created by: Robot Team                                         *
@rem * Created 2019.9.26                                                *
@rem **********************************************************************
@echo off
set CUR=%CD%
set SCRIPT_DIR=%~dp0
@rem driver type java1.0 or java2.0
set DRIVER_TYPE=%1
@rem target or xml path
set TARGET=%2
@rem robot pid
set ROBOT_PID=%3
@rem socket port
set SOCKET_PORT=%4
set JAVA_HOME=%JAVA_HOME%
set PATH=%PATH%

set JRE=%5
if EXIST %JRE% set JAVA_HOME=%JRE%
if EXIST %JRE% set PATH=.;%JRE%\bin;%PATH%
cd /d %SCRIPT_DIR%
java -XX:+StartAttachListener -jar HuaweiRpa-0.0.1-SNAPSHOT.jar "%DRIVER_TYPE%" "%TARGET%" "%ROBOT_PID%" "%SOCKET_PORT%"
cd /d %CUR%