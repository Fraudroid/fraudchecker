# encoding:utf-8
import json
import xlwt
import os


def deal(filepath, outexcelpath):
    # filepath = 'D:\\PaperW\\Stage2\\droidData\\4600out0\\out\\'
    # outexcelpath = 'D:\\PaperW\\Stage2\\result\\4600\\0-800new.xls'
    sep = os.path.sep
    fraud_type = ['Interaction Fraud', 'Non-interaction Fraud', 'Pop-window Fraud', 'Hidden Fraud', 'Size Fraud',
                  'Overlap Fraud', 'Number Fraud']
    pathDir = os.listdir(filepath)
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('sheet', cell_overwrite_ok=True)
    for i in range(len(fraud_type) + 1):
        sheet.col(i).width = 500 * 20
    sheet.write(0, 0, 'MD5')
    for i, ft in enumerate(fraud_type):
        sheet.write(0, i + 1, ft)
    line_number = 1
    for allDir in pathDir:
        apk_name = allDir[allDir.rfind(sep, 1, len(allDir) - 1) + 1:allDir.rfind('.json', 1)]
        child = os.path.join('%s//%s' % (filepath, allDir))
        if (child.endswith('json')):
            f = open(child)
            jsonfile = f.read()
            json_content = json.loads(jsonfile)
            json_dict = json_content
            # print json_dict
            for ft, state in json_dict.iteritems():
                if len(state) != 0:
                    temp = ''
                    for i, c in enumerate(state):
                        if i < len(state) - 1:
                            temp += c + ','
                        else:
                            temp += c
                    print temp
                    sheet.write(line_number, fraud_type.index(str(ft)) + 1, temp)
            # temps = ''
            # for k, v in json_dict.iteritems():
            #     if len(v) != 0:
            #         temps = temps + k + ','
            # print apk_name
            # print temps
            # sheet.write(line_number, 0, apk_name)
            # sheet.write(line_number, 2, temps)
            sheet.write(line_number, 0, apk_name)
            line_number += 1
    book.save(outexcelpath)
