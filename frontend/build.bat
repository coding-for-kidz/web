@ECHO OFF
npx webpack
cd util
python compile_css.py
cd ..
