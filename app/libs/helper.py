def is_isbn_or_key(word):
    """
    word:普通关键字搜索
    对URL进行判断
    """
    isbn_or_key = 'key'  # 默认设为key
    if len(word) == 13 and word.isdigit():  # 字符串isdigit（）方法判断是否全为数字
        isbn_or_key = 'isbn'
    short_word = word.replace('_', '')
    if '_' in word and len(short_word) == 10 and short_word.isdigit:
        isbn_or_key = 'isbn'
    return isbn_or_key

