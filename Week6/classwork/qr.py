import qrcode

img = qrcode.make("https://www.youtube.com/realpolya")
img.save("qr.png", "PNG")
