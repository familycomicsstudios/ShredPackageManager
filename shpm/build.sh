rm dist/*
cp ../.config/pip/pip.conf.3 ../.config/pip/pip.conf
python3 -m build
cp ../.config/pip/pip.conf.2 ../.config/pip/pip.conf
cd dist
pip install shpm_themadpunter-*\.whl --force-reinstall
cd ../..
cp shpm/shpm.sh venv/bin/shpm
chmod +x venv/bin/shpm
