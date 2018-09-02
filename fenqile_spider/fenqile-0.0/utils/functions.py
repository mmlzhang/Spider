
from lxml import etree


def etree_xpath(html, xpath):
    """
    使用 etree 匹配需要的数据

    :param html: 页面的 html utf-8格式
    :param xpath:  匹配的 xpath
    :return: 匹配结果列表  list
    """
    etree_obj = etree.HTML(html)
    result_list = etree_obj.xpath(xpath)
    return result_list


