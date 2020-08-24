import sys
import streamlit.cli as stcli
import os

target_path = os.path.join(os.path.dirname(__file__), 'app.py')

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", target_path, "--global.developmentMode=false"]
    sys.exit(stcli.main())