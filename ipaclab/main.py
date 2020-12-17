from ipaclab.crawler import ScriptScraper


def main():
    """여기다가 코드 작성하세요~"""
    c1 = ScriptScraper(is_assigned='voucher16', is_transcripted=2)
    c1.do_crawler(start_page=0)


if __name__ == '__main__':
    main()