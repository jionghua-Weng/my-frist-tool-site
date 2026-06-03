export default async function(request) {
  var url = new URL(request.url);
  var text = url.searchParams.get('text');
  if (!text || text.length > 200) {
    return new Response('Bad request', { status: 400 });
  }

  var ttsUrl = 'https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q=' + encodeURIComponent(text);

  try {
    var res = await fetch(ttsUrl, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    if (!res.ok) return new Response('Upstream error ' + res.status, { status: 502 });
    var buf = await res.arrayBuffer();
    return new Response(buf, {
      status: 200,
      headers: {
        'Content-Type': 'audio/mpeg',
        'Cache-Control': 'public, max-age=86400'
      }
    });
  } catch (e) {
    return new Response('Error: ' + e.message, { status: 502 });
  }
}
