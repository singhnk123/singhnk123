


from PIL import Image, ImageEnhance, ImageFilter

ASCII = "@%#*+=-:. "

img = Image.open(r"C:\Users\Neekhil kumar singh\Desktop\neekhilsingh\assets\profile.jpeg")

# Crop only head + upper shoulders
w, h = img.size
img = img.crop((220, 80, w-220, h-220))

# Grayscale
img = img.convert("L")

# Increase sharpness for eyes
img = ImageEnhance.Sharpness(img).enhance(2.5)

# Increase contrast
img = ImageEnhance.Contrast(img).enhance(3.0)

# Slight blur removes beard/neck noise
img = img.filter(ImageFilter.GaussianBlur(radius=0.6))

# Thresholding removes unnecessary dots
pixels = img.load()
for y in range(img.height):
    for x in range(img.width):
        p = pixels[x, y]

        # Make background pure white
        if p > 180:
            pixels[x, y] = 255

        # Remove weak beard noise
        elif p > 120:
            pixels[x, y] = 170

        # Darken eyes, eyebrows, hair
        elif p < 80:
            pixels[x, y] = 0

WIDTH = 68
ratio = img.height / img.width
HEIGHT = int(WIDTH * ratio * 0.52)

img = img.resize((WIDTH, HEIGHT))

pixels = img.getdata()

chars = "".join(
    ASCII[p * (len(ASCII)-1) // 255]
    for p in pixels
)

ascii_img = ""

for i in range(0, len(chars), WIDTH):
    line = chars[i:i+WIDTH]

    # remove mostly empty lines
    if line.count(" ") < WIDTH-4:
        ascii_img += line.rstrip() + "\n"

with open("ascii.txt", "w", encoding="utf-8") as f:
    f.write(ascii_img)

print(ascii_img)
