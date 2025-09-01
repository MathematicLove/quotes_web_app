#!/usr/bin/env bash
set -e
TITLE="$1"
QUOTE="$2"

: "${GOOGLE_API_KEY:?Set GOOGLE_API_KEY in env}"
: "${GOOGLE_CSE_ID:?Set GOOGLE_CSE_ID in env}"

IMG_URL=$(curl -s "https://www.googleapis.com/customsearch/v1?searchType=image&key=${GOOGLE_API_KEY}&cx=${GOOGLE_CSE_ID}&q=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "$TITLE")" \
  | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['items'][0]['link']) if 'items' in data and data['items'] else print('')")

[ -z "$IMG_URL" ] && echo "Image not found" && exit 1

OUT="side_by_side.html"
cat > "$OUT" <<HTML
<!doctype html><meta charset="utf-8">
<title>${TITLE} — цитата</title>
<style>
  body{font-family:system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;margin:0}
  .wrap{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:24px}
  blockquote{font-size:28px;line-height:1.3;margin:0}
  img{max-width:100%;border-radius:16px}
</style>
<div class="wrap">
  <div><blockquote>“${QUOTE}”</blockquote><p>— ${TITLE}</p></div>
  <div><img src="${IMG_URL}" alt="image of ${TITLE}"></div>
</div>
HTML

echo "Saved to ${OUT}"
