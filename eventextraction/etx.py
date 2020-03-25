#!/usr/bin/env python3
# 代码原作者： lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# 原作者项目地址： https://github.com/liuhuanyong/ComplexEventExtraction
# 大邓封装成包第三方包，【公众号:大邓和他的Python】
import re

'''中文复句整理及模板'''
class EventsExtraction:
    """
    可以用来识别文本说话风格。风格识别包括因果、顺承、反转、条件。
    """
    def __init__(self):
        self.but_wds = self.pattern_but()
        self.seq_wds = self.pattern_seq()
        self.condition_wds = self.pattern_condition()
        self.more_wds = self.pattern_more()

        self.but_patterns = self.create_pattern(self.but_wds)
        self.seq_patterns = self.create_pattern(self.seq_wds)
        self.condition_patterns = self.create_pattern(self.condition_wds)
        self.more_patterns = self.create_pattern(self.more_wds)


    def pattern_but(self):
        """
        定义转折事件模式
        :return: 返回模式词组

        例如
        extractor = EventsExtraction()
        but_words = extractor.pattern_but()
        print(but_words)
        >>>
        [[['与其'], ['不如'],'but'],
        [['虽然','尽管','虽'],['但也','但还','但却','但'],'but'],
        [['虽然','尽管','虽'],[ '但','但是也','但是还','但是却',],'but'],
        [['不是'],['而是'],'but'],
        ...

        """
        wds = [[['与其'], ['不如'],'but'],
                [['虽然','尽管','虽'],['但也','但还','但却','但'],'but'],
                [['虽然','尽管','虽'],[ '但','但是也','但是还','但是却',],'but'],
                [['不是'],['而是'],'but'],
                [['即使','就算是'],['也','还'],'but'],
                [['即便'],['也','还'],'but'],
                [['虽然','即使'],['但是','可是','然而','仍然','还是','也', '但'],'but'],
                [['虽然','尽管','固然'],['也','还','却'],'but'],
                [['与其','宁可'],['决不','也不','也要'],'but'],
                [['与其','宁肯'],['决不','也要','也不'],'but'],
                [['与其','宁愿'],['也不','决不','也要'],'but'],
                [['虽然','尽管','固然'],['也','还','却'],'but'],
                [['不管','不论','无论','即使'],['都', '也', '总', '始终', '一直'],'but'],
                [['虽'],['可是','倒','但','可','却','还是','但是'],'but'],
                [['虽然','纵然','即使'],['倒','还是','但是','但','可是','可','却'],'but'],
                [['虽说'],['还是','但','但是','可是','可','却'],'but'],
                [['无论'],['都','也','还','仍然','总','始终','一直'],'but'],
                [['与其'],['宁可','不如','宁肯','宁愿'],'but']]

        return wds

    def pattern_seq(self):
        """
        定义顺承事件模式
        :return:  返回模式词组


        例如
        extractor = EventsExtraction()
        seq_words = extractor.pattern_seq()
        print(seq_words)
        >>>
        [
            [['又', '再', '才', '并'], ['进而'], 'sequence'],
            [['首先', '第一'], ['其次', '然后'], 'sequence'],
            [['首先', '先是'], ['再', '又', '还', '才'], 'sequence'],
            [['一方面'], ['另一方面', '又', '也', '还'], 'sequence']]
        ]
        """
        wds =[
            [['又', '再', '才', '并'], ['进而'], 'sequence'],
            [['首先', '第一'], ['其次', '然后'], 'sequence'],
            [['首先', '先是'], ['再', '又', '还', '才'], 'sequence'],
            [['一方面'], ['另一方面', '又', '也', '还'], 'sequence']]

        return wds


    def pattern_more(self):
        """
        定义并列事件模式
        :return:  返回模式词组

        例如
        extractor = EventsExtraction()
        more_words = extractor.pattern_more()
        print(more_words)
        >>>
        [
                [['不但', '不仅'], ['并且'], 'more'],
                [['不单'], ['而且', '并且', '也', '还'], 'more'],
                [['不但'], ['而且', '并且', '也', '还'], 'more'],
                [['不管'], ['都', '也', '总', '始终', '一直'], 'more']
        ]
        """
        wds = [
                [['不但', '不仅'], ['并且'], 'more'],
                [['不单'], ['而且', '并且', '也', '还'], 'more'],
                [['不但'], ['而且', '并且', '也', '还'], 'more'],
                [['不管'], ['都', '也', '总', '始终', '一直'], 'more'],
                [['不光'], ['而且', '并且', '也', '还'], 'more'],
                [['虽然', '尽管'], ['不过'], 'more'],
                [['不仅'], ['还', '而且', '并且', '也'], 'more'],
                [['不论'], ['还是', '也', '总', '都', '始终', '一直'], 'more'],
                [['不只'], ['而且', '也', '并且', '还'], 'more'],
                [['不但', '不仅', '不光', '不只'], ['而且'], 'more'],
                [['尚且', '都', '也', '又', '更'], ['还', '又'], 'more'],
                [['既然', '既',], ['就', '便', '那', '那么', '也', '还'], 'more'],
                [['无论', '不管', '不论', '或'], ['或'], 'choice'],
                [['或是'], ['或是'], 'choice'],
                [['或者', '无论', '不管', '不论'], ['或者'], 'choice'],
                [['不是'], ['也'], 'choice'],
                [['要么', '或者'], ['要么', '或者'], 'choice'],
        ]
        return wds


    def pattern_condition(self):
        """
        定义条件事件模式
        :return: 返回模式词组

        例如
        extractor = EventsExtraction()
        condition_words = extractor.pattern_condition()
        print(condition_words)
        >>>
        [
                [['除非'], ['否则', '才', '不然', '要不'], 'condition'],
                [['除非'], ['否则的话'], 'condition'],
                [['还是', '无论', '不管'], ['还是', '都', '总'], 'condition'],
                [['既然'], ['又', '且', '也', '亦'], 'condition'],
        ]

        """
        wds = [
                [['除非'], ['否则', '才', '不然', '要不'], 'condition'],
                [['除非'], ['否则的话'], 'condition'],
                [['还是', '无论', '不管'], ['还是', '都', '总'], 'condition'],
                [['既然'], ['又', '且', '也', '亦'], 'condition'],
                [['假如'], ['那么', '就', '也', '还'], 'condition'],
                [['假若', '如果'], ['那么', '就', '那', '则', '便'], 'condition'],
                [['假使', '如果'], ['那么', '就', '那', '则', '便'], 'condition'],
                [['尽管', '如果'], ['那么', '就', '那', '则', '便'], 'condition'],
                [['即使', '就是'], ['也', '还是'], 'condition'],
                [['如果', '既然'], ['那么'], 'condition'],
                [['如', '假设'], ['则', '那么', '就', '那'], 'condition'],
                [['如果', '假设'], ['那么', '则', '就', '那'], 'condition'],
                [['万一'], ['那么', '就'], 'condition'],
                [['要是', '如果'], ['就', '那'], 'condition'],
                [['要是', '如果', '假如'], ['那么', '就', '那', '的话'], 'condition'],
                [['一旦'], ['就'], 'condition'],
                [['既然', '假如', '既', '如果'], ['则','就'], 'condition'],
                [['只要'], ['就', '便', '都', '总'], 'condition'],
                [['只有'], ['才', '还'], 'condition'],

        ]
        return wds


    def create_pattern(self, wds):
        """
        编译模式
        :param wds: 模式词组
        :return: 模式s

        例如
        extractor = EventsExtraction()
        seq_wds = extractor.pattern_seq()
        print(extractor.create_pattern(seq_wds))
        >>>
        [re.compile('(又|再|才|并)(.*)(进而)([^？?！!。；;：:\\n\\r,，]*)'),
        re.compile('(首先|第一)(.*)(其次|然后)([^？?！!。；;：:\\n\\r,，]*)'),
        re.compile('(首先|先是)(.*)(再|又|还|才)([^？?！!。；;：:\\n\\r,，]*)'),
        re.compile('(一方面)(.*)(另一方面|又|也|还)([^？?！!。；;：:\\n\\r,，]*)')]

        """
        patterns = []
        for wd in wds:
            pre = wd[0]
            pos = wd[1]
            pattern = re.compile(r'({0})(.*)({1})([^？?！!。；;：:\n\r,，]*)'.format('|'.join(pre), '|'.join(pos)))
            patterns.append(pattern)
        return patterns


    def split_sents(self, content):
        """
        文章分句处理, 切分长句，冒号，分号，感叹号等做维护标识
        :param content: 文本
        :return:  句子列表


        例如
        extractor = EventsExtraction()
        content = '虽然你做了坏事，但我觉得你是好人。一旦时机成熟，就坚决推行'
        sents = extractor.split_sents(content)
        print(sents)
        >>>
        ['虽然你做了坏事，但我觉得你是好人',
         '一旦时机成熟，就坚决推行']
        """
        return [sentence.replace('　','') for sentence in re.split(r'[？?！!。；;：:\n\r]', content) if sentence]


    def pattern_match(self, patterns, sent):
        """
        模式匹配
        :param patterns:  正则表达式模式，即create_pattern生产的pattern
        :param sent:  句子
        :return:
        """
        datas = {}
        max = 0
        for p in patterns:
            ress = p.findall(sent)
            if ress:
                for res in ress:
                    data = {'pre_wd': res[0], 'pre_part': res[1], 'post_wd': res[2], 'post_part ': res[3]}
                    len_res = len(res[0] + res[2])
                    if len_res > max:
                        datas = data
                        max = len_res
        return datas

    def extract_tuples(self, sent):
        """
        基于模式，抽取出相应的四元组
        :param sent:
        :return:
        """
        but_tuples = self.pattern_match(self.but_patterns, sent)
        condition_tuples = self.pattern_match(self.condition_patterns, sent)
        seq_tuples = self.pattern_match(self.seq_patterns, sent)
        more_tuples = self.pattern_match(self.more_patterns, sent)

        return but_tuples, condition_tuples, seq_tuples, more_tuples


    def extract_main(self, content):
        """
        处理主函数
        :param content:
        :return:

        例如
        extractor = EventsExtraction()
        datas = extractor.extract_main('虽然你做了坏事，但我觉得你是好人。一旦时机成熟，就坚决推行')
        print(datas)
        >>>[{'sent': '虽然你做了坏事，但我觉得你是好人', 'type': 'but', 'tuples': {'pre_wd': '虽然', 'pre_part': '你做了坏事，', 'post_wd': '但', 'post_part ': '我觉得你是好人'}},
            {'sent': '一旦时机成熟，就坚决推行', 'type': 'condition', 'tuples': {'pre_wd': '一旦', 'pre_part': '时机成熟，', 'post_wd': '就', 'post_part ': '坚决推行'}}]
        """
        sents = self.split_sents(content)
        datas = []
        for sent in sents:
            data = {}
            data['sent'] = sent
            but_tuples, condition_tuples, seq_tuples, more_tuples = self.extract_tuples(sent)
            if but_tuples:
                data['type'] = 'but'
                data['tuples'] = but_tuples
            if condition_tuples:
                data['type'] = 'condition'
                data['tuples'] = condition_tuples
            if seq_tuples:
                data['type'] = 'seq'
                data['tuples'] = seq_tuples
            if more_tuples:
                data['type'] = 'more'
                data['tuples'] = more_tuples
            if 'type' in data:
                datas.append(data)
        return datas

    def stats(self, datas):
        """
        统计文本中各种风格句子的个数
        :param datas:  extract_main处理后得到的datas
        :return: 字典

        例如
        extractor = EventsExtraction()
        datas = extractor.extract_main('虽然你做了坏事，但我觉得你是好人。一旦时机成熟，就坚决推行')
        print(extractor.stats(datas))
        >>>{'but': 1, 'condition': 1, 'seq': 0, 'more': 0, 'other': 0}
        """
        but, condition, seq, more, other = 0,0,0,0,0
        for data in datas:
            if data['type']=='but':
                but+=1
            elif data['type']=='condition':
                condition+=1
            elif data['type']=='seq':
                seq+=1
            elif data['type']=='more':
                more+=1
            else:
                other+=1
        return {'but':but, 'condition':condition, 'seq':seq, 'more':more, 'other':other}








#extractor = EventsExtraction()
#datas = extractor.extract_main('虽然你做了坏事，但我觉得你是好人。一旦时机成熟，就坚决推行')
#print(extractor.stats(datas))
