# -*- coding:utf-8 -*-
# author:lvao
# datetime:2019/5/29 14:12
# software: PyCharm


HEADERS = {
    'Origin': 'http://www.dianping.com',
    'Referer': 'http://www.dianping.com/shop/69089926',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
}

CSS_FILE_REGEX = r'href="(//s3plus.*?svgtextcss.*?css)"'
LOCATION_REGEX = r'.(.*?){background:(.*?)px(.*?)px;}'
SVG_FILE_REGEX = 'class\^="(.*?)"\]{width:(.*?)px.*?url(.*?);.*?}'
SVG_INFO_REGEX = r'<text\sx="0"\sy="(\d+)">(.*?)</text>'

# 需要woff字体解密的tag, 有新改动的tag直接在里面删除或者添加就可以了
WOFF_TO_DECRYPT = [r'<d\sclass="num">(.*?)</d>', r'<e\sclass="adress">(.*?)</e>',
                   r'<svgmtsi\sclass="shopdesc">(.*?)</svgmtsi>']

# 需要svg字体解密的tag
SVG_TO_DECRYPT = ['<svgmtsi class="(.*?)"></svgmtsi>']

RIGHT_FONT_TAG = ['<svgmtsi class="{}">{}</svgmtsi>']