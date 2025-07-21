from io import BytesIO
from PIL import Image

'''
php code 
$imageWidth = $image->width();
$imageHeigth = $image->height();

if ($imageWidth >= $imageHeigth) {
            // оригинальную ширину делаим на 10
    $watermarkSizeWidth = round($imageWidth / 10);
    $watermarkSource->scale(width: $watermarkSizeWidth);

    // top left
    $propWidth = 1035;
    $propWidthTop = 42;
    $top = $imageWidth * $propWidthTop / $propWidth;

    $propHeigth = 963;
    $propHeigthTop = 59;
    $left = $imageHeigth * $propHeigthTop / $propHeigth;

}
'''

class WatermarkPhoto:
    def __init__(self, watermark_path) -> None:
        self.watermark_path = watermark_path

    def add_watermark(self, image_bytes) -> BytesIO:
       
        if isinstance(image_bytes, BytesIO):
            image_bytes.seek(0)
            image = Image.open(image_bytes).convert("RGBA")
        else:
            image = Image.open(BytesIO(image_bytes)).convert("RGBA")


        watermark = Image.open(self.watermark_path).convert("RGBA")
        ratio = min(image.size[0] / 10 / watermark.size[0], image.size[1] / 10 / watermark.size[1])
        new_size = (int(watermark.size[0] * ratio), int(watermark.size[1] * ratio))
        watermark = watermark.resize(new_size)

        # print(f"ratio: {ratio}")
        # print(f"watermark size: {new_size}")
        # print(watermark)

        imageWidth = image.width
        imageHeigth = image.height
        if imageWidth >= imageHeigth:
            print(f"imageWidth >= imageHeigth: ")
        else:
            print("imageHeigth >= imageWidth")
        
        position = (10, 10)  # top-left
        transparent = Image.new('RGBA', image.size)
        transparent.paste(image, (0, 0))
        transparent.paste(watermark, position, mask=watermark)
        output = BytesIO()
        transparent.convert('RGB').save(output, 'JPEG')
        output.seek(0)
        return output