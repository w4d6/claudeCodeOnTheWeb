#!/usr/bin/env python3
"""
Yahoo!ニュースから新着記事を取得するスクリプト
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import sys


def scrape_yahoo_news(num_articles=5):
    """
    Yahoo!ニュースのトピックスから新着記事を取得

    Args:
        num_articles: 取得する記事数（デフォルト: 5）

    Returns:
        記事のリスト
    """
    url = "https://news.yahoo.co.jp/"

    try:
        # ヘッダーを設定してリクエスト
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, 'html.parser')

        articles = []

        # トピックス記事を取得
        # Yahoo!ニュースのトピックス部分から記事を抽出
        topics = soup.select('a[class*="newsFeed_item_link"]')

        if not topics:
            # 別のセレクターを試す
            topics = soup.select('.newsFeed_item_link')

        if not topics:
            # さらに別の方法を試す - より一般的なセレクター
            topics = soup.find_all('a', href=True)
            topics = [t for t in topics if '/articles/' in t.get('href', '')]

        for i, topic in enumerate(topics[:num_articles]):
            try:
                title = topic.get_text(strip=True)
                link = topic.get('href', '')

                # 相対URLの場合は絶対URLに変換
                if link.startswith('/'):
                    link = 'https://news.yahoo.co.jp' + link

                if title and link:
                    articles.append({
                        'title': title,
                        'url': link,
                        'scraped_at': datetime.now().isoformat()
                    })

                    if len(articles) >= num_articles:
                        break

            except Exception as e:
                print(f"記事の解析エラー: {e}", file=sys.stderr)
                continue

        return articles

    except requests.RequestException as e:
        print(f"リクエストエラー: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"予期しないエラー: {e}", file=sys.stderr)
        return []


def save_articles(articles, filename='yahoo_news.json'):
    """
    記事をJSONファイルに保存

    Args:
        articles: 記事のリスト
        filename: 保存先ファイル名
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'count': len(articles),
            'articles': articles
        }, f, ensure_ascii=False, indent=2)


def main():
    """メイン処理"""
    print("Yahoo!ニュースから新着記事を取得中...")

    articles = scrape_yahoo_news(num_articles=5)

    if not articles:
        print("記事を取得できませんでした", file=sys.stderr)
        sys.exit(1)

    print(f"\n{len(articles)}件の記事を取得しました:\n")

    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   URL: {article['url']}\n")

    # JSONファイルに保存
    save_articles(articles)
    print(f"記事をyahoo_news.jsonに保存しました")


if __name__ == '__main__':
    main()
