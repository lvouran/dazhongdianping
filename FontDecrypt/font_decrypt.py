# -*- coding:utf-8 -*-
# author:lvao
# datetime:2019/5/29 12:41
# software: PyCharm
# 大众点评网站字体破解
# 主要思路: 找到对应的css文件将里面的内容做成一个字典，然后获取里面

import re
from get_res import get_response
from lxml import etree
from settings import *


class SvgFontDecrypt(object):
    def __init__(self, detail_url, html_text=None):
        self.detail_url = detail_url
        self.html_text = html_text
        if not html_text:
            self.html_text = self.get_html_text(self.detail_url)
        self.css_url = self.get_css_url()
        self.css_dict = {}
        self.svg_dict = {}

    def get_css_url(self):
        try:
            return re.search(CSS_FILE_REGEX, self.html_text).group(1)
        except Exception as e:
            print(f'{e}\t文件中没有找到svg对应的字体文件,检查文件内容或者css文件提取规则...')
            return None

    def get_html_text(self, detail_url):
        html_text = get_response(detail_url)
        if html_text.status_code != 200:
            print(f'{self.detail_url}返回的状态码不为200, 考虑ip被封...')
            return ''
        return html_text.text

    def create_location_dict(self):
        css_text = get_response(self.css_url)
        css_info_list = re.findall(LOCATION_REGEX, css_text.text)
        for css_attribute, x, y in css_info_list:
            if 'url' in css_attribute:
                css_attribute = css_attribute.split('.')[-1]
            self.css_dict.update({css_attribute: (float(x.replace('-', '')), float(y.replace('-', '')))})
        print(self.css_dict)
        _svg_info_list = re.findall(SVG_FILE_REGEX, css_text.text)
        for svg_arrtibute, font_width, svg_url in _svg_info_list:
            # 获取svg的内容
            self.svg_dict.update({svg_arrtibute: {'font_width': int(font_width),
                                  'svg_url': svg_url.replace('(', '').replace(')', '')}})

    def create_svg_dict(self):
        # 获取svg_url里面的内容 并更新字典
        for _v in self.svg_dict.values():
            svg_html = get_response(_v.get('svg_url', ''))
            _svg_info_list = re.findall(SVG_INFO_REGEX, svg_html.text)
            for y, svg_text in _svg_info_list:
                _v.update({int(y): svg_text})

    def overwrite_html_for_svg(self):
        # 从页面里面获取加密的属性，然后进行找到对应的字体，重新写入
        for svg_to_decrypt in SVG_TO_DECRYPT:
            html_svg_list = re.findall(svg_to_decrypt, self.html_text)[1:]
            for html_svg in html_svg_list:
                svg_x, svg_y = self.css_dict.get(html_svg)
                for _key in self.svg_dict.keys():
                    if html_svg.startswith(_key):
                        _index = svg_x // self.svg_dict.get(_key).get('font_width')
                        right_font = self.find_right_font(int(svg_y), _key, _index)
                        for right_font_tag in RIGHT_FONT_TAG:
                            self.html_text = re.sub(right_font_tag.format(html_svg, ''),
                                                    right_font_tag.format(html_svg, right_font), self.html_text)

    def find_right_font(self, y, key, _index):
        _dict = self.svg_dict.get(key)
        for k, v in _dict.items():
            if not isinstance(k, str):
                if y < k:
                    return _dict.get(k)[int(_index)]

    def pase_html(self):
        print(self.html_text)
        HTML = etree.HTML(self.html_text)
        phone_num_list = HTML.xpath('//span[@class="info-name"]')
        phone_num_list = phone_num_list[0].xpath('string(.)')
        print('未解密的电话:\t' + ''.join(phone_num_list))
        comment_tag_list = HTML.xpath('//p[@class="desc"]')
        for comment_list in comment_tag_list:
            comment = comment_list.xpath('string(.)')
            print(f'解密后的评论:\t{comment}\n')


class WoffFontDecrypt(object):
    # 需要做手动下载woff字体，然后做基础的unicode编码和utf编码的映射，
    # 通过正则获取到所有的&#x(.*?);  之后进行反向替换，获取到完整的html
    def __init__(self):
        pass




if __name__ == '__main__':
    test = SvgFontDecrypt('http://www.dianping.com/shop/75187097')
    test.create_location_dict()
    test.create_svg_dict()
    test.overwrite_html_for_svg()
    test.pase_html()
