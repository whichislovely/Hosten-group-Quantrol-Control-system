@echo OFF
set "MSYSTEM=CLANG64"
"C:\msys64\msys2_shell.cmd" -c "artiq_run set_slow_dds_states.py"