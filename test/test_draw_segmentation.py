import base64
import numpy as np
from PIL import Image
import io
import matplotlib.pyplot as plt

# Base64 string
base64_string = "iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAAAAAB5Gfe6AAADWklEQVR42u3dy3KDQAxE0f7/n+4sklRl4UdszwhpbmuZBagPAg+YcqQmZQtb/il4fCqAA5D8ZADDAZK/MH9DZlcCdBy0wvwtz7TCAWh5qXEdQMtrbfJXAdhsAPcE8KPauqcB+b11R+T8og1A09P/WX5v2U3bW4Ca/K3uiVwCcHeb10/FtfmvXxaWDMCdDbe4KtYf/14A5Zf/QQOwcQ+3/twtf9El5vTjf3/rLVaF1x3/Jk9Frsnf6LGQ956hfqXo+a8Q2NycXy56/mKBhvlLBfZ2ZR8EUBe/UiD5t/XiAeOvjf2MyK/k75a/4RKo9PC3XAKV5ne//K+3ZQ8R2NOXfSbAv9vzguqb/3lvhgN4DsCO3mw2wKT4O5aqo/KvBzAkv+df/bcMwKz06wE8DWBxm+OO/2KAcfHXAgyMv/SBxcT8KwFo+T3+8rd2AEbGXzgAuOPvey/3Ygbgb8fM/PMB3AlAgwEMHYBbL/ex8nvYs98tADZ4ADw5/xoAswfA9AEIAP0McAYgAAEIwMz8AcADKAABgAMoAHQA4QGEBxAeQHiACGQE8ADCAygAdADhASKQEcADKAB0AOEBFAA6gPAACgAdQHgABYAOIDyAAkAHUADoAAoAHUB4AAUgAHAABYAOoADQARQAOoACQAdQAAIABxA9fwAUgADAARSAAMABFIAAwAEUgACw85cJ0AEEB5DYAsICqHn2vQCaUgEIAPwsMF3AdIEARCAAAQhAPgizFCIvhzEA91pj5H/QHQHgYYPn53/SIvX4/7Z5/AD4ooLHz29GwOM7vx2V34+j58/PiNLz58ek4fHzXyXyj1XY6a8AsNkAZgPYaAAbDWCjAWw0gI0GsNEANhnATn4wgI0GsANABrDJAJ5T9Pw7BGw2gE0W8MSCx19H4MEFj79AwPMLHv8zgvf2dgzA23s7QuCjHc0/Cz7cScfrwAsIC4wnXw/XbHfqR8OyLc38gFw4USMXCcj8HwAcs4Z8o+lDH54tXVIMFFi7nhp4u/Tg1ub4G8lbPbOeJPxpmfkckf4lSgS2fJNGzz/0hiBfpeddirxNlLcJKQKg98l1ecHjX6mgXsVOX0ygpsVOX0Sg5sVOv1dAYwoe/9vgB+ImzxtEOrTY6f/HIEjB49/EWLa9L+I1MzpkwzY7AAAAAElFTkSuQmCC"

# Decode base64
img_data = base64.b64decode(base64_string)

# Convert to image
img = Image.open(io.BytesIO(img_data))
mask = np.array(img)

# Display
plt.figure(figsize=(8, 8))
plt.imshow(mask, cmap='gray')
plt.title('Object: the objects\nBbox: [433, 86, 908, 550]')
plt.axis('off')
plt.show()

print(f"Image shape: {mask.shape}")