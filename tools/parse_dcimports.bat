set /P PPYTHON_PATH=<../PPYTHON_PATH

cd..

%PPYTHON_PATH% tools\parse_dcimports.py -o "otp/distributed/DCClassImports.py" "astron/dclass/united.dc"
