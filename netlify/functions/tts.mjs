exports.handler = async function(event) {
  const text = event.queryStringParameters?.text;
  if (!text || text.length > 200) {
    return { statusCode: 400, body: 'Missing or too long text' };
  }

  const url = 'https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q=' + encodeURIComponent(text);

  try {
    const res = await fetch(url, {
      headers: { 'User-Agent': 'Mozilla/5.0' }
    });
    if (!res.ok) throw new Error('Upstream ' + res.status);
    const buf = Buffer.from(await res.arrayBuffer());
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'audio/mpeg',
        'Cache-Control': 'public, max-age=86400'
      },
      body: buf.toString('base64'),
      isBase64Encoded: true
    };
  } catch (e) {
    return { statusCode: 502, body: 'TTS proxy error: ' + e.message };
  }
};
