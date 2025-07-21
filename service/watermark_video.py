import ffmpeg
from io import BytesIO
import tempfile
import os

'''
public static function addVideoComp($path){
        ini_set('memory_limit', -1);
        $time = time();
        $savePatch = public_path('video/' . $time . '.mp4');
        $ffmpeg = \FFMpeg\FFMpeg::create();
        $video = $ffmpeg->open($path);
        $width = $video->getStreams()->videos()->first()->getDimensions()->getWidth();
        $height = $video->getStreams()->videos()->first()->getDimensions()->getHeight();
        $property=self::getProperty($width,$height);

        $waterMarkUrl = public_path() . '/images/logo.png';
        $waterVideo=public_path() . '/images/logo_'.$property['widthW'].'.png';

        if(!file_exists($waterVideo)){
            $manager = ImageManager::gd();
            $watermarkSource = $manager->read($waterMarkUrl);
            $watermarkSource->scale(width: $property['widthW']);
            $watermarkSource->toPng()->save($waterVideo);
        }
        $video
            ->filters()
            ->watermark($waterVideo, array(
                'position' => 'relative',
                'top' => $property['top'],
                'left' => $property['left'],
            ));
        $video
            ->save(new \FFMpeg\Format\Video\X264(), $savePatch);
        return $savePatch;
}
получить размеры видео
$width
$height
переделай эту пхп функцию на python
public static function getProperty($width,$height){
        $res=[
            'top'=>0,
            'left'=>0,
            'widthW'=>0,
            'heightW'=>0,
        ];
        if ($width >= $height) {
            $res['widthW'] = (int)round($width / 10,0);

            // top left
            $propWidth = 1035;
            $propWidthTop = 42;
            $res['top'] = $width * $propWidthTop / $propWidth;

            $propHeigth = 963;
            $propHeigthTop = 59;
            $res['left'] = $height * $propHeigthTop / $propHeigth;

        }else{
            $res['widthW'] = round($height / 10);

            $propHeigth = 1035;
            $propHeigthTop = 42;
            $res['top'] = $height * $propHeigthTop / $propHeigth;

            $propWidth = 963;
            $propWidthTop = 59;
            $res['left'] = $width * $propWidthTop / $propWidth;

        }
        return $res;
}
потом ватермарк    $watermarkSource->scale(width: $property['widthW']);
и изменить его позицию
$video
            ->filters()
            ->watermark($waterVideo, array(
                'position' => 'relative',
                'top' => $property['top'],
                'left' => $property['left'],
));
'''

class WatermarkKVideo:
    def __init__(self, watermark_path) -> None:
        self.watermark_path = watermark_path

    def add_watermark(self, video_bytes) -> BytesIO:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
            temp_video.write(video_bytes.read())
            temp_video_path = temp_video.name

        width,height = self.get_video_size(temp_video_path)
        property = self.get_property(width,height)
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_output:
            temp_output_path = temp_output.name
        try:
            input_video = ffmpeg.input(temp_video_path)
            input_logo = ffmpeg.input(self.watermark_path)

            scaled_logo = input_logo.filter('scale', property['widthW'], -1)
            out = ffmpeg.overlay(input_video, scaled_logo, x=int(property['left']), y=int(property['top']))
            (
                ffmpeg
                .output(out, temp_output_path, vcodec='libx264', acodec='aac', strict='experimental')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            print("====== FFMPEG STDERR ======")
            print(e.stderr.decode('utf8'))
            print("===========================")
            raise RuntimeError('FFmpeg command failed')            

        with open(temp_output_path, 'rb') as f:
            output_bytes = BytesIO(f.read())

        os.remove(temp_video_path)
        os.remove(temp_output_path)

        output_bytes.seek(0)
        return output_bytes

    def get_property(self, width, height):
        res = {
            'top': 0,
            'left': 0,
            'widthW': 0,
            'heightW': 0,  
        }

        if width >= height:
            res['widthW'] = round(width / 10)

            prop_width = 1035
            prop_width_top = 42
            res['top'] = width * prop_width_top / prop_width

            prop_height = 963
            prop_height_top = 59
            res['left'] = height * prop_height_top / prop_height

        else:
            res['widthW'] = round(height / 10)

            prop_height = 1035
            prop_height_top = 42
            res['top'] = height * prop_height_top / prop_height

            prop_width = 963
            prop_width_top = 59
            res['left'] = width * prop_width_top / prop_width

        return res 

    def get_video_size(self, video_path):
        probe = ffmpeg.probe(video_path)
        video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
        if not video_streams:
            raise Exception('No video stream found')
        width = int(video_streams[0]['width'])
        height = int(video_streams[0]['height'])
        return width, height