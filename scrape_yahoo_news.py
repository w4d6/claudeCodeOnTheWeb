#!/usr/bin/env python3
"""
Yahoo!ニュースから新着記事を取得するスクリプト
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import sys
import re
import os


def clean_title(title):
    """
    記事タイトルから不要な情報を削除

    Args:
        title: 元のタイトル

    Returns:
        クリーニングされたタイトル
    """
    if not title:
        return title

    # 先頭の数字を削除（例：「1」「2」など）
    title = re.sub(r'^\d+', '', title)

    # 末尾の配信元と日時情報を削除（複数パターンに対応）
    # パターン1: 「東スポWEB11/6(木)14:55」「スポーツ報知11/6(木)12:20」
    title = re.sub(r'[^\s　]+\d{1,2}/\d{1,2}\([月火水木金土日]\)\d{1,2}:\d{2}.*$', '', title)

    # パターン2: 残った配信元情報（全角・半角スペース + カタカナ・漢字の組み合わせ + 日付）
    title = re.sub(r'[　\s][^\s　]*[^\s　]*\d{1,2}/\d{1,2}.*$', '', title)

    # パターン3: タイムスタンプのみが残っている場合
    title = re.sub(r'\d{1,2}:\d{2}.*$', '', title)

    # 前後の空白を削除
    title = title.strip()

    return title


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

        for i, topic in enumerate(topics):
            try:
                title = topic.get_text(strip=True)
                # タイトルをクリーニング
                title = clean_title(title)
                link = topic.get('href', '')

                # 相対URLの場合は絶対URLに変換
                if link.startswith('/'):
                    link = 'https://news.yahoo.co.jp' + link

                # タイトルとURLが有効で、タイトルが十分な長さの場合のみ追加
                if title and link and len(title) > 10:
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

    # JSONファイルに保存（実行時間をファイル名に含める）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'yahoo_news_{timestamp}.json'
    save_articles(articles, filename)
    print(f"記事を{filename}に保存しました")
    print(f"保存場所: {os.path.abspath(filename)}")


if __name__ == '__main__':
    main()
