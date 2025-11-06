# Yahoo News Scraper

Yahoo!ニュースから新着記事を取得するスクリプトとGitHub Actionsによる定期実行の設定です。

## 機能

- Yahoo!ニュースのトップページから新着記事を5件取得
- 記事のタイトルとURLを抽出
- JSON形式で保存
- GitHub Actionsによる自動実行

## ローカルでの実行

### 必要なパッケージのインストール

```bash
pip install -r requirements.txt
```

### スクリプトの実行

```bash
python scrape_yahoo_news.py
```

実行すると、`yahoo_news.json` に結果が保存されます。

## GitHub Actionsによる定期実行

このリポジトリには GitHub Actions のワークフローが設定されています：

- **定期実行**: 毎日午前9時（日本時間）に自動実行
- **手動実行**: GitHub のActions タブから手動で実行可能
- **プッシュ時**: main ブランチや claude/ プレフィックスのブランチへのプッシュ時に実行

### 実行結果の確認

1. GitHubリポジトリの「Actions」タブを開く
2. 「Yahoo News Scraper」ワークフローを選択
3. 各実行の詳細を確認
4. Artifacts から `yahoo-news-*` をダウンロードして結果を確認

## 出力形式

```json
{
  "timestamp": "2025-11-06T12:00:00.000000",
  "count": 5,
  "articles": [
    {
      "title": "記事タイトル",
      "url": "https://news.yahoo.co.jp/...",
      "scraped_at": "2025-11-06T12:00:00.000000"
    }
  ]
}
```

## 設定のカスタマイズ

### 取得する記事数の変更

`scrape_yahoo_news.py` の以下の行を変更：

```python
articles = scrape_yahoo_news(num_articles=5)  # 数値を変更
```

### 実行スケジュールの変更

`.github/workflows/scrape_news.yml` の cron 設定を変更：

```yaml
schedule:
  - cron: '0 0 * * *'  # 毎日 0:00 UTC (9:00 JST)
```

## 依存パッケージ

- requests: HTTPリクエスト
- beautifulsoup4: HTMLパース
- lxml: HTMLパーサー

## ライセンス

MIT
