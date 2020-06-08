#!/bin/sh

n=3
echo '[1/'$n'] Modifying files for creating application'
sed '1 s/^/from fbs_runtime.application_context.PyQt5 import ApplicationContext\n/' final.py > main.py
sed '/if __name__ == /a\    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext ' main.py -i
sed '/    sys.exit(app.exec_())/c\    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()' main.py -i
echo '    sys.exit(exit_code)' >> main.py
# changing location of image resource(s)
sed 's/"logo_banner.png"/appctxt.get_resource("logo_banner.png")/g' main.py -i

# todo remove print statements in code

echo '[2/'$n'] Creating fbs project'
fbs startproject
cp main.py src/main/python/
cp mechanismClass.py src/main/python/
cp analytical.py src/main/python/
mkdir src/main/resources/
mkdir src/main/resources/base/
cp logo_banner.png src/main/resources/base/
cp -r icons src/main/

echo '[3/'$n'] Starting application'
fbs run
fbs freeze --debug
fbs installer 

# fbs release