from execution_files.py_files.packages import *
from time import time

start_time = time()

os.system('python execution_files/py_files/1_divide_pages.py')
os.system('python execution_files/py_files/2_identify_panels.py')
os.system('python execution_files/py_files/3_bubbles_to_text.py')
os.system('python execution_files/py_files/4_img_to_nlp.py')
os.system('python execution_files/py_files/5_translate.py')
os.system('python execution_files/py_files/6_tts.py')

elapsed_time = time() - start_time

print(f"El proceso ha tardado: {elapsed_time}")

print("ENHORABUENA, YA SE PUEDE ESCUCHAR ESTE HISTORIA VISUL !!")