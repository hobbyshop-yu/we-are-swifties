---
description: 曲記事ページの作成手順と品質要件
---

# 曲記事ページ作成ワークフロー

## リファレンス
- **手本ファイル**: `opalite.html`（最も完成度が高い記事）
- **サイトルート**: `c:\Users\81808\Desktop\Weareスウィフティーズ`

## ページ構成（上から順番に）

### 1. `<head>` セクション
```
- charset, viewport
- google-site-verification メタタグ
- <title>: "Taylor Swift - {曲名} 歌詞・和訳・徹底解説 | We are Swifties"
- <meta description>: 曲の概要（日本語）
- Google Fonts: Noto Sans JP, Playfair Display, Inter
- CSS変数（:root）: 曲ごとの色テーマ（下記「色テーマ」参照）
- OGP / Twitter Card メタタグ（og:image はYouTubeサムネ）
- GA4 トラッキングスクリプト (G-PESZB0HW0B)
```

### 2. グローバルナビゲーション
```html
<nav class="global-nav">
    <a href="index.html" class="nav-home">We are Swifties</a>
    <a href="index.html">曲一覧</a>
    <a href="about.html">運営者情報</a>
    <a href="contact.html">お問い合わせ</a>
</nav>
```

### 3. ヒーローセクション
```
- .hero-label: アルバム名（例: "The Life of a Showgirl"）
- .hero-title: 曲タイトル（グラデーション文字）
- .hero-artist: "Taylor Swift"（イタリック）
- .hero-album: アルバム名タグ（ピル型ボーダー）
- 背景: radial-gradient のオーロラ効果 + shimmerアニメーション
- フローティングパーティクル（gem要素 4個、曲テーマ色）
```

### 4. `<main>` 内の構成

#### a. 戻るリンク
```html
<a href="index.html" class="back-link">← 曲一覧に戻る</a>
```

#### b. Song Intro（曲紹介カード）
```
- song-intro: ボーダー付きカード
- h2: 曲の日本語概要タイトル
- p: 曲の背景・テーマの説明（2-3段落）
- .keyword: 重要キーワードをハイライト
```

#### c. 凡例（Legend）
```html
<div class="legend">
    <div class="legend-item">
        <div class="legend-dot en"></div>
        <span class="legend-label en">English Lyrics</span>
    </div>
    <div class="legend-item">
        <div class="legend-dot ja"></div>
        <span class="legend-label ja">日本語訳</span>
    </div>
    <div class="legend-item">
        <div class="legend-dot cm"></div>
        <span class="legend-label cm">Commentary</span>
    </div>
</div>
```

#### d. YouTube埋め込み
```html
<div class="youtube-section">
    <h2>▶ Official Video / Lyric Video</h2>
    <div class="youtube-wrapper">
        <iframe src="https://www.youtube.com/embed/{VIDEO_ID}"
            title="{曲名}" allow="..." allowfullscreen></iframe>
    </div>
</div>
```
- **注意**: 動画IDは必ず実在する公式/公認動画のものを使う
- Taylor Swift公式チャンネルの動画を優先
- 存在しない場合はlyric videoを使用

#### e. 歌詞セクション（全歌詞を掲載）
```
繰り返し構造:
  - .section-header: セクション名（VERSE 1, PRE-CHORUS, CHORUS, VERSE 2, BRIDGE, OUTRO等）
  - .lyric-block > .lyric-pair: 英語歌詞 + 日本語訳（1行ずつペア）
  - .commentary: セクションごとの解説コメント（アイコン + テキスト）
```

##### 歌詞の要件 ⚠️ 重要
- **全歌詞を掲載する**（ハイライトや抜粋ではなく完全版）
- 各セクション（VERSE 1, PRE-CHORUS, CHORUS, VERSE 2, BRIDGE, OUTRO等）を漏れなく含む
- コーラスの繰り返しも省略せず掲載
- 歌詞ソースは公式歌詞サイト（Genius, AZLyrics等）で確認
- 和訳は直訳ではなく自然な意訳（ニュアンスを重視）

##### コメンタリーの要件
- 各セクションに1つ以上のコメンタリーを付ける
- アイコン（絵文字）を先頭に付ける
- 内容: 歌詞の背景、メタファーの解説、文化的参照、テイラーの過去作品との関連
- 参照元（インタビュー、ファン考察）があれば明記

### 5. マスコットトリビアセクション（`</main>`の前）
```html
<!-- mascot-section は <main> タグの中、article-footer の前に配置 -->
<section class="mascot-section">
    <div class="mascot-card">
        <img class="mascot-img" id="mascot-image" src="images/cat-guitar.png" alt="Mascot">
        <div class="mascot-bubble">
            <p class="trivia-label">🐱 Did You Know?</p>
            <p id="mascot-text">Loading...</p>
        </div>
    </div>
</section>
```
- マスコット画像は `images/cat-guitar.png`, `images/cat-piano.png`, `images/cat-mic.png` の3種
- トリビアは **曲に関連する豆知識を5-6個** 用意
- `<script>` でランダム表示（ページ末尾）

### 6. フッター（`</main>`の前、マスコットの後）
```html
<footer class="article-footer">
    <p class="site-name">We are Swifties</p>
    <div class="footer-links">
        <a href="index.html">ホーム</a>
        <a href="about.html">運営者情報</a>
        <a href="contact.html">お問い合わせ</a>
        <a href="privacy-policy.html">プライバシーポリシー</a>
    </div>
    <p class="copyright">© 2026 We are Swifties. All rights reserved.</p>
</footer>
```

### 7. トリビアスクリプト（`</main>`の後、`</html>`の前）
```javascript
<script>
    const triviaList = [
        { img: 'images/cat-piano.png', text: '曲に関連する豆知識1' },
        { img: 'images/cat-guitar.png', text: '曲に関連する豆知識2' },
        // ... 5-6個
    ];
    const pick = triviaList[Math.floor(Math.random() * triviaList.length)];
    document.getElementById('mascot-image').src = pick.img;
    document.getElementById('mascot-text').textContent = pick.text;
</script>
```

## 色テーマのルール

各曲は独自のカラーテーマを持つ。CSS変数で定義する。

### 例（opalite.html）
```css
--accent-opal: #4dd9e8;        /* メインアクセント色 */
--accent-opal-light: #7ae8f4;  /* ライトアクセント色 */
--english-color: #7ae8f4;      /* 英語歌詞の色 */
--japanese-color: #d4f5fa;      /* 日本語訳の色 */
--commentary-color: #4a6a78;    /* コメンタリーの色 */
--gradient-opal: linear-gradient(...); /* グラデーション */
```

### index.htmlのカード色
- 各曲のカードは `.song-card.{曲クラス名}` で色を定義
- `border-color`, `hover border-color`, `box-shadow`, `.card-arrow color` を曲テーマで統一
- **曲のテーマカラーをカードの文字色・ボーダー色に反映させる**

## index.html への追加

新しい曲を追加する際は:
1. アルバムセクション（`album-header` + 曲カード群）を追加
2. カードCSS（`.song-card.{クラス名}`）を `</style>` の前に追加
3. `sitemap.xml` に新ページのURLを追加

## デプロイ手順
// turbo-all
1. `git add -A`
2. `git commit -m "{変更内容}"`
3. `git push`
