import csv
import json
import re
import jieba
import jieba.analyse
import pandas as pd
import pymongo

"""
TODO:
- 添加异常处理
- 完善注释
- 添加日志
- 抽象成一个类
"""

def get_all_text(filename):
    """取出所有评价的句子
    """
    comment_list = []
    with open(filename) as f:
        rows = csv.reader(f)
        for row in rows:
            one_comment = row[-1]
            comment_list.append(one_comment)

    return ''.join(comment_list[1:]) 


def cut_text(all_text, stop_words_path='stop_words.txt'):
    """找到评价中重要关键词
    ERROR:
    jieba: path does not exist: stop_words.txt
    使用os.path.join, 或config去定义文件路径
    """
    # https://github.com/fxsjy/jieba
    jieba.analyse.set_stop_words(stop_words_path)
    text_tags = jieba.analyse.extract_tags(all_text, topK=30)
    return text_tags


def get_bad_words(text_tags, all_text):
    """根据关键词找到对应的句子
    """
    words = {}
    for tag in text_tags:
        tag_re = re.compile(f'(\w*{tag}\w*)')
        # print(tag_re.findall(all_text))
        words[tag] = tag_re.findall(all_text)
    return words


def get_comment(txt):
    text_tags = cut_text(txt)
#     print(text_tags)
    words = get_bad_words(text_tags, txt)
#     print(txt, words, len(words))
#     for k, v in words.items():
#         print(k, '-->', len(v), v)
    return words



def get_result(db):
    """
    从db获取数据，返回json
    """
    result = []
    try:
        # sort first
        name_list = sorted(db.list_collection_names())
        print('all result:', name_list)
        for name in name_list:
            col = db.get_collection(name)
            item = {}
            data = pd.DataFrame(list(col.find()))
            item['productId'] = name
            item['name'] = ' '.join(data.referenceName[0].split()[:3])
            item['size'] = data.groupby(['productSize']).count().to_dict()['days']
            
            comment_by_size = {}
            comment_d = data.groupby(['productSize'])['content'].apply(lambda x: ','.join(x)).to_dict()

            for size, txt in comment_d.items():    
                comment = get_comment(txt)  # only 1 size
                comment_by_size[size] = comment
            
        #     print(comment_by_size)
            item['color'] = data.groupby(['productColor']).count().to_dict()['days']
            item['comment'] = comment_by_size

            result.append(item)
    except Exception as e:    
        print(e)

    # print(result[:3])
    # 注意：转换格式，从numpy int64 to python int
    result = pd.Series(result).to_json(orient='values')
    # json to list
    result = json.loads(result)
    return result


def main1():
    all_text = get_all_text('db.csv')
    # print(all_text)
    text_tags = cut_text(all_text)
    print(text_tags)
    words = get_bad_words(text_tags, all_text)
    for k, v in words.items():
        print(k, '-->', len(v), v)


def main():
    c = pymongo.MongoClient()
    db = c.get_database('chaping')
    get_result(db)


if __name__ == '__main__':
    main()