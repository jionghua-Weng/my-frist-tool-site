<?php
/**
 * TTS 代理：调用百度翻译 TTS (UK English)，返回 MP3 音频。
 * 用法：tts.php?q=hello+world
 */
header('Access-Control-Allow-Origin: *');
header('Content-Type: audio/mpeg');

$text = isset($_GET['q']) ? trim($_GET['q']) : '';
if ($text === '') {
    http_response_code(400);
    header('Content-Type: text/plain');
    echo 'missing q parameter';
    exit;
}

if (mb_strlen($text) > 300) {
    $text = mb_substr($text, 0, 300);
}

$url = 'https://fanyi.baidu.com/gettts?lan=uk&text=' . urlencode($text) . '&spd=3&source=web';

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer: https://fanyi.baidu.com/',
    'Accept: audio/mpeg,audio/*',
]);

$audio = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode !== 200 || !$audio || strlen($audio) < 100) {
    http_response_code(502);
    header('Content-Type: text/plain');
    echo 'tts error: ' . $httpCode;
    exit;
}

header('Content-Length: ' . strlen($audio));
header('Cache-Control: public, max-age=86400');
echo $audio;
