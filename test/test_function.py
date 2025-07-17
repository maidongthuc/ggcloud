import sys
import os

# Thêm đường dẫn root project vào sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api.fire_extinguisher.fire_extinguisher import process_single_image
objects="CO2 fire extinguisher (without a pressure gauge) | Powder fire extinguisher (with pressure gauge) | clock of fire extinguisher | Fire extinguisher tray"
url_image = "http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752564039.png"
print(process_single_image(url_image, objects, index=0, http_request=None))