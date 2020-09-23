# -*- coding: utf-8 -*-
import json
import sys

# AIMind  NER 加载

# {"annotation":{"result":[{"endOffset":5,"text":"霍英东","type":"人物","color":"#19be6b","beginOffset":2},{"endOffset":10,"text":"霍震宇","type":"人物","color":"#19be6b","beginOffset":7},{"endOffset":43,"text":"三子","type":"关系","color":"#BE8319","beginOffset":41},{"endOffset":73,"text":"霍震霆","type":"人物","color":"#19be6b","beginOffset":70}],"selectionColorObj":[{"index":"霍英东-2-5","endOffset":5,"text":"霍英东","color":"#19be6b","type":"人物","beginOffset":2},{"index":"霍震宇-7-10","endOffset":10,"text":"霍震宇","color":"#19be6b","type":"人物","beginOffset":7},{"index":"三子-41-43","endOffset":43,"text":"三子","color":"#BE8319","type":"关系","beginOffset":41},{"index":"霍震霆-70-73","endOffset":73,"text":"霍震霆","color":"#19be6b","type":"人物","beginOffset":70}],"source":"﻿<霍英东, 霍震宇, 三子>\t据此间媒体11日报道，<e1>霍英东</e1>长房三子<e2>霍震宇</e2>再度入禀法院，要求法官颁令兄长霍震霆交出记录<e1>霍英东</e1>所有资产及财务资料的记事本1.0"},"source":"content://﻿<霍英东, 霍震宇, 三子>\t据此间媒体11日报道，<e1>霍英东</e1>长房三子<e2>霍震宇</e2>再度入禀法院，要求法官颁令兄长霍震霆交出记录<e1>霍英东</e1>所有资产及财务资料的记事本1.0","mark":true}


# TO BI0

import argparse


def bio_sent(sent, ner_list):
    bio_list = ['O'] * len(sent)
    for item in ner_list:
        subj = item[0]
        type = item[-1]
        for i in range(0, len(sent) - len(subj) + 1):
            if sent[i:i + len(subj)] == subj:
                bio_list[i] = 'B-' + type
                for j in range(1, len(subj)):
                    bio_list[i + j] = 'I-' + type
    return sent, bio_list


def load_ner(input, output):
    with open(output, 'w', encoding='utf-8') as f:
        with open(input, 'r', encoding='utf-8') as input_fs:
            for i, line in enumerate(input_fs):
                data = line.strip()
                if len(data) == 0:
                    continue
                data = json.loads(data)
                question = data.get("text").strip()
                ner_list = []
                for item in data["event_list"]:
                    ner_list.append([item.get("trigger"), item.get("event_type")])
                sent, bio_list = bio_sent(question, ner_list)
                for char, tag in zip(sent, bio_list):
                    if not char:
                        print(sent)
                    f.write(char + ' ' + tag + '\n')
                f.write('\n')


parser = argparse.ArgumentParser(description='AIMind NER Data Loader')
parser.add_argument('--input', action="store", default="data/dev.json", type=str)
parser.add_argument('--output', action="store", default="data/dev-bio.txt", type=str)

if __name__ == '__main__':
    args = parser.parse_args()
    load_ner(args.input, args.output)
