#!/usr/bin/env python
"""
Simple script to run the Django server
"""

import os
import sys
import subprocess

def main():
    """Run the Django development server"""
    try:
        # Change to the correct directory
        os.chdir(r'C:\Users\ghimi\OneDrive\Desktop\Kinmel_Eccomerce_APP')
        
        # Activate virtual environment and run server
        if os.name == 'nt':  # Windows
            activate_script = r'venv\Scripts\activate.bat'
            cmd = f'{activate_script} && python manage.py runserver 8000'
            subprocess.run(cmd, shell=True)
        else:  # Unix/Linux
            cmd = 'source venv/bin/activate && python manage.py runserver 8000'
            subprocess.run(cmd, shell=True)
            
    except Exception as e:
        print(f"Error running server: {e}")

if __name__ == '__main__':
    main()
