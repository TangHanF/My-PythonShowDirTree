# -*- coding:utf-8 -*-

import os

from pyecharts import Bar

template_dir = "<div style='font-weight:bold;font-size:16px'>{save_file_name}</div>"
template_file = "<div style:'color:red'>" \
                "<a href='{link_dir}' title={title} style='color:red;text-decoration:none'>{save_file_name}</a>" \
                "<span style='font-size:8px;color:#2196f3'>({file_size})</span>" \
                "</div>"
template_report = "<div style='padding-top:60px'></div><div>" \
                  "<span style='color:green;font-weight:bold;font-size=14px'>总共扫描{scan_count}次</span><br>" \
                  "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#452345;font-size=9px'>目录：{scan_dir_count}个</span><br>" \
                  "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#452345;font-size=9px'>文件：{scan_file_count}个</span>" \
                  "</div>"
template_report_charts = "<div style='padding-top:60px'>{}</div>"

file_type_dict = {"Word文档": [".doc", ".docx"], "Excel文件": [".xls", ".xlsx"], "PDF文件": [".pdf"], "图片": [".jpg", ".bmp", ".gif", ".jpeg", ".png"],
                  "视频": [".mp4"], "音频": [".mp3", ".wav"], "文本文件": [".txt"], "java文件": [".java"], "xml文件": [".xml"], "html文件": [".html", ".htm"],
                  "JS文件": [".js"], "css文件": [".css"], "jsp文件": [".jsp"], "压缩文件": [".zip", ".rar", ".7z"]

                  }
# 注意顺序要和file_type_dict的键顺序一致
file_type_list_list = ["Word文档", "Excel文件", "PDF文件", "图片", "视频", "音频", "文本文件", "java文件", "xml文件",
                       "html文件", "JS文件", "css文件", "jsp文件", "压缩文件"]

filter_list = []
report_dir_count = 0
report_file_count = 0
report_scan_count = 0


class Report():
    word = excel = pdf = img = video = sound = txt = java = xml = html = css = js = jsp = zip = 0

    def __init__(self):
        pass

    def count(self, type_):
        if type_ == "Word文档":
            self.word += 1
        elif type_ == "Excel文件":
            self.excel += 1
        elif type_ == "PDF文件":
            self.pdf += 1
        elif type_ == "图片":
            self.img += 1
        elif type_ == "视频":
            self.video += 1
        elif type_ == "音频":
            self.sound += 1
        elif type_ == "文本文件":
            self.txt += 1
        elif type_ == "java文件":
            self.java += 1
        elif type_ == "xml文件":
            self.xml += 1
        elif type_ == "html文件":
            self.html += 1
        elif type_ == "JS文件":
            self.js += 1
        elif type_ == "css文件":
            self.css += 1
        elif type_ == "jsp文件":
            self.jsp += 1
        elif type_ == "压缩文件":
            self.zip += 1


def create_report(dir_, report):
    bar = Bar(title="{}文件类型分布图".format(dir_), subtitle="文件类型分布情况", width=1024, height=768, page_title="文件类型分布图")
    bar.add("文件类型分布图", file_type_list_list, [report.word, report.excel, report.pdf, report.img, report.video, report.sound, report.txt,
                                             report.java, report.xml, report.html, report.js, report.css, report.jsp, report.zip],
            mark_line=["average"], mark_point=["max", "min"])
    bar.render(path="文件类型分布图.html")
    file = open("文件类型分布图.html", encoding="utf-8")
    str = ""
    for line in file.readlines():
        str += line
    return str


def is_list_item_in_str(list_, str_):
    """
    判断list集合中某项存在于字符串
    :param list_:
    :param str_:
    :return: True:包含
    """
    index_ = 0
    for val in list_:
        if str(str_).find(val) == -1:
            continue
        else:
            index_ += 1
    if index_ > 0:
        return True
    else:
        return False


def show_dir(start_path, file_name):
    report = Report()
    if start_path == "":
        return
    if file_name == "":
        return
    if os.path.splitext(file_name)[1] == "":
        file_name += ".html"
    file_path = file_name
    file_save = open(file_name, "w", encoding="utf-8")
    global report_scan_count, report_dir_count, report_file_count
    for root, dirs, files in os.walk(start_path):
        report_scan_count += 1
        if (is_list_item_in_str(filter_list, root)) is True:
            print(">>>>>>>>>>>>>>>> 忽略：", root)
            continue
        else:
            print("正在处理：", root)
        report_dir_count += 1
        level = root.replace(start_path, "").count(os.sep)
        indent = "---" * 1 * level
        tmp = os.path.abspath(root)
        str_1 = "{}{}".format(indent, os.path.abspath(root).replace(start_path + os.sep, "")) + "\n"
        file_save.write(template_dir.format(save_file_name=str_1))
        sub_indent = "&nbsp;&nbsp;&nbsp;" * 1 * (level + 1)

        for f in files:
            file_type = os.path.splitext(f)[1]
            for val in file_type_dict:
                if file_type in file_type_dict[val]:
                    report.count(val)

            report_file_count += 1
            if (is_list_item_in_str(filter_list, os.path.split(root)[1])) is True:
                continue
            str_2 = "|{}{}".format(sub_indent, f) + "\n"
            full_path = tmp + os.sep + f
            unit = "MB"
            calc_file_size = round(os.path.getsize(full_path) / float(pow(1024, 2)), 2)

            file_save.write(template_file.format(save_file_name=str_2, file_size=str(calc_file_size) + unit, link_dir=full_path, title=full_path))
    file_save.write(template_report.format(scan_count=report_scan_count, scan_dir_count=report_dir_count, scan_file_count=report_file_count))

    s = create_report(start_path, report)
    file_save.write(template_report_charts.format(s))
    file_save.close()
    os.system(file_path)


if __name__ == "__main__":
    file = open("filter_list.txt", encoding="utf-8")
    for line in file.readlines():
        filter_list.append(line.replace("\n", ""))
    file.close()
    # show_dir("I:\\Python_Test", "test")
    show_dir("G:\\资料文档\\山东光辉", "test")
    # show_dir("G:\\System", "test")
    # show_dir("G:\\soft", "test")
    # show_dir("D:\\project\\pshtA_rep", "test")
