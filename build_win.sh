#!/bin/bash

# cleanup
python3 build.py --action build --os win --skip_disabled_templates --build_stage cleanup

# bring in modules from other repos
# This section must be updated based on version.json
cd /d/rapidcloud-modules/rc-aws-net; git fetch --all; git reset --hard v1.0.2
cd /d/rapidcloud-modules/rc-aws-eks; git fetch --all; git reset --hard v0.0.1
cd /d/rapidcloud-core

python3 build.py --action build --os win --skip_disabled_templates --build_stage add_external_modules

# run pyinstaller 
KEY=`cat pyinstaller-key.txt`
ADD_DATA="--add-data terraform/templates;terraform/templates"
HIDDEN_IMPORTS="--hidden-import pymssql"
for module in commands/modules/*; do
    if test -f "$module/module.json"; then
        ADD_DATA="$ADD_DATA --add-data $module/module.json;$module"
        HIDDEN_IMPORTS="$HIDDEN_IMPORTS --hidden-import ${module////.}"
    fi
done
pyinstaller --clean \
    $ADD_DATA \
    --key $KEY \
    $HIDDEN_IMPORTS \
    --collect-all pyfiglet \
    --log-level=DEBUG \
    kc --onefile

# copy required files
python3 build.py --action build --os win --skip_disabled_templates --build_stage copy_files > build_copy_files.log

# sign kc.exe
read -p  "Did you sign kc.exe? [yes, no]: " proceed
if [ $proceed != 'yes' ]
then
    exit 0
fi

# build and upload zip files
python3 build.py --action build --os win --skip_disabled_templates --build_stage build_and_upload_zip > build_build_and_upload_zip.log

# remove external modules
python3 build.py --action build --os win --skip_disabled_templates --build_stage remove_external_modules > build_remove_external_modules.log

