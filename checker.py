# encoding:utf-8
import json
import os
import sys

type_count = 8
# path = 'D:\\PaperW\\Stage2\\data\\tjmusic\\'
# path = 'D:\\PaperW\\Stage2\\data\\2017_01_10\\2017_01_10\\overlap\\'
path = ''
output_path = ''
trans_path = ''
filepath = ''
activity_dict = {}
main_activity = 'null'
first_activity = 'null'
json_dict = {}
json_tag_list = []
trans_file = ''
sep = os.path.sep


def read_files():
    global trans_file
    t = open(trans_path)
    trans_file = t.read()
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s//%s' % (filepath, allDir))
        if (child.endswith('json')):
            f = open(child)
            jsonfile = f.read()
            json_content = json.loads(jsonfile)
            json_dict[json_content['tag']] = jsonfile


def whoisnext(tag):
    trans_content = json.loads(trans_file)
    for i in range(len(trans_content)):
        if (trans_content[i][1] == tag):
            return trans_content[i][2]


def whoisbefore(tag):
    trans_content = json.loads(trans_file)
    for i in range(len(trans_content)):
        if (trans_content[i][2] == tag):
            return trans_content[i][1]


def ad_ex_by_traffic():
    for jsonfile in json_dict.values():
        json_content = json.loads(jsonfile)
        if (json_content['tag'] == first_activity):
            if 'current_traffic' not in json_content:
                return True
            if int(json_content['current_traffic']) > 0:
                # print int(json_content['current_traffic'])
                return True
            else:
                return False


def get_activity(json_list):
    global main_activity
    global first_activity
    tag_dict = {}
    for jsonfile in json_dict.values():
        json_content = json.loads(jsonfile)
        # activity = json_content['foreground_activity'][0:json_content['foreground_activity'].rfind('/', 1)]
        tag_dict[json_content['tag']] = int(json_content['tag'][json_content['tag'].rfind('_', 1) + 1:])
        # if activity in activity_dict.keys():
        #     activity_dict[activity] += 1
        # else:
        #     activity_dict[activity] = 1
    sorted_tag = sorted(tag_dict.items(), key=lambda d: d[1], reverse=False)
    first_activity = sorted_tag[0][0]
    # print first_activity
    # second_activity = sorted_tag[1][0]
    for jsonfile in json_dict.values():
        json_content = json.loads(jsonfile)
        if (json_content['tag'] == first_activity):
            main_activity = json_content['foreground_activity'][0:json_content['foreground_activity'].rfind('/', 1)]

    id = 1
    while 'launcher' in str(main_activity) or 'android.settings' in str(main_activity) or 'packageinstaller' in str(
            main_activity) or 'allpaper.livepicker' in str(main_activity) or 'cyanogenmod.trebuchet' in str(
        main_activity) or 'com.chillingo' in str(main_activity) or 'android.browser' in str(main_activity):
        for jsonfile in json_dict.values():
            json_content = json.loads(jsonfile)
            if (id == len(sorted_tag)):
                print('THIS RESULT IS ERROR!')
                return
            if (json_content['tag'] == sorted_tag[id][0]):
                main_activity = json_content['foreground_activity'][0:json_content['foreground_activity'].rfind('/', 1)]
        id += 1


def is_in_views(json_content, view):
    for i in range(len(json_content['views'])):
        if (json_content['views'][i]['class'] == view):
            return True
    return False


def results_via_matrix(origin_matrix, type, threshold):
    index_matrix = []
    loc = 0
    for i in origin_matrix[type - 1]:
        if (i >= threshold):
            index_matrix.append(loc)
        loc += 1
    print('Type %s' % type)
    if (len(index_matrix) == 0): print("None")
    result_list = []
    for l in index_matrix:
        result_list.append(json_tag_list[l])
        print(json_tag_list[l])
    print
    return type, result_list


def output_result(fraud_mark_matrix):
    result_dict = {}
    none_flag = 0
    type, result = results_via_matrix(fraud_mark_matrix, 1, 1)
    result_dict['Interaction Fraud'] = result
    if (len(result) != 0): none_flag = 1
    type, result = results_via_matrix(fraud_mark_matrix, 2, 4)
    result_dict['Non-interaction Fraud'] = result
    if (len(result) != 0): none_flag = 1
    type, result = results_via_matrix(fraud_mark_matrix, 3, 1)
    result_dict['Hidden Fraud'] = result
    if (len(result) != 0): none_flag = 1
    type, result = results_via_matrix(fraud_mark_matrix, 4, 1)
    result_dict['Size Fraud'] = result
    if (len(result) != 0): none_flag = 1
    type, result = results_via_matrix(fraud_mark_matrix, 5, 1)
    result_dict['Overlap Fraud'] = result
    if (len(result) != 0): none_flag = 1
    type, result = results_via_matrix(fraud_mark_matrix, 6, 1)
    result_dict['Number Fraud'] = result
    if (len(result) != 0): none_flag = 1
    type, result = results_via_matrix(fraud_mark_matrix, 7, 1)
    result_dict['Pop-window Fraud'] = result
    if (len(result) != 0): none_flag = 1
    apk_name = path[path.rfind(sep, 1, len(path) - 1) + 1:path.rfind(sep, 1)]
    if (none_flag == 1):
        f = open(output_path + apk_name + '.json', 'w')
        json.dump(result_dict, f, indent=1, sort_keys=True)
    return result_dict


def ad_picker2(json):
    # 根据resource_id或者class的内容判断是否是广告+webview判断
    is_ad_indices = [0] * len(json['views'])
    webview_ad_ext = 0
    # webview判断
    # 获取framesize,frame
    frame_size = json['views'][0]['size']
    ftemp_list = frame_size.split('*')
    a = int(ftemp_list[0])
    b = int(ftemp_list[1])
    fwidth = a
    fheight = b
    frame_size = a * b
    div3 = fheight / 3
    Fx1 = json['views'][0]['bounds'][0][0]
    Fy1 = json['views'][0]['bounds'][0][1]
    Fx2 = json['views'][0]['bounds'][1][0]
    Fy2 = json['views'][0]['bounds'][1][1]
    Frange1 = Fy1 + div3
    Frange2 = Fy1 + div3 * 2
    Fctx = Fx1 + fwidth / 2
    Fcty = Fy1 + fheight / 2
    for i in range(len(json['views'])):
        # 如果view是web，判断大小。
        if (json['views'][i]['class'] == 'android.webkit.WebView'):
            web_size = json['views'][i]['size']
            wtemp_size = web_size.split('*')
            aw = int(wtemp_size[0])
            bw = int(wtemp_size[1])
            web_size = aw * bw
            if (web_size * 2 <= frame_size):
                is_ad_indices[i] = 1
                webview_ad_ext = 1
    # hahahaha
    if (webview_ad_ext == 1):
        return is_ad_indices
    for i in range(len(json['views'])):
        if 'ad' in json['views'][i]['class'] or 'Ad' in json['views'][i]['class']:
            is_ad_indices[i] = 1
        if 'Ad' in json['views'][i]['resource_id']:
            is_ad_indices[i] = 1
        if json['views'][i]['resource_id'] == 'id/0x1' and json['views'][i]['class'] == 'android.widget.LinearLayout':
            is_ad_indices[i] = 1
    # filter
    for (vnum, isview) in enumerate(is_ad_indices):
        if isview == 1:
            vsize = json['views'][vnum]['size']
            temp_list = vsize.split('*')
            a = int(temp_list[0])
            b = int(temp_list[1])
            vsize = a * b
            if (vsize != frame_size and vsize * 1.5 > frame_size):
                is_ad_indices[vnum] = 0
    return is_ad_indices


def ad_picker3(json):
    is_ad_indices = [0] * len(json['views'])
    child_tree = []

    def rules(i):
        if json['views'][i]['class'] == None:
            return False
        if 'ad' in json['views'][i]['class'] or 'Ad' in json['views'][i]['class']:
            return True
        if json['views'][i]['resource_id'] == None:
            return False
        if 'Ad' in json['views'][i]['resource_id']:
            return True
        if json['views'][i]['resource_id'] == 'id/0x1' and 'Layout' in json['views'][i]['class']:
            return True
        if 'id/0x8765' in json['views'][i]['resource_id'] and 'Layout' in json['views'][i]['class']:
            return True

        # if json['views'][i]['resource_id'] == 'id/content' and 'Layout' in json['views'][i]['class']:
        #     return True
        return False

    def traverse(root):
        child_list = json['views'][root]['children']
        if (len(child_list) == 0):
            return
        child_tree.extend(child_list)
        for child in child_list:
            traverse(child)

    def check_position(imageview):
        image_size = imageview['size']
        itemp_list = image_size.split('*')
        ai = int(itemp_list[0])
        bi = int(itemp_list[1])
        Iwidth = ai
        Iheight = bi
        image_size = ai * bi
        Ix1 = imageview['bounds'][0][0]
        Iy1 = imageview['bounds'][0][1]
        Ix2 = imageview['bounds'][1][0]
        Iy2 = imageview['bounds'][1][1]
        # 针对条型Image
        if (Iwidth >= fwidth * 0.9 and Iy2 < Frange1):
            return True
        elif (Iwidth >= fwidth * 0.9 and Iy1 > Frange2):
            return True
        # 针对中央型Image
        wdiv2 = Iwidth / 2
        hdiv2 = Iheight / 2
        Ictx = Ix1 + wdiv2
        Icty = Iy1 + hdiv2
        if (((Ictx - Fctx) ** 2 + (
                    Icty - Fcty) ** 2) ** 0.5 <= 50 and image_size * 13 >= frame_size and image_size * 2 <= frame_size):
            return True
        # 针对全屏型Image
        if (frame_size * 0.93 <= image_size and len(views_list) <= 2):
            return True
        return False

    # webview判断
    views_list = []
    for i in range(1, len(json['views'])):
        if i not in views_list:
            views_list.append(json['views'][i]['class'])
    # 获取framesize,frame
    frame_size = json['views'][0]['size']
    ftemp_list = frame_size.split('*')
    a = int(ftemp_list[0])
    b = int(ftemp_list[1])
    fwidth = a
    fheight = b
    frame_size = a * b
    div3 = fheight / 3
    Fx1 = json['views'][0]['bounds'][0][0]
    Fy1 = json['views'][0]['bounds'][0][1]
    Fx2 = json['views'][0]['bounds'][1][0]
    Fy2 = json['views'][0]['bounds'][1][1]
    Frange1 = Fy1 + div3
    Frange2 = Fy1 + div3 * 2
    Fctx = Fx1 + fwidth / 2
    Fcty = Fy1 + fheight / 2

    for v in range(len(json['views'])):
        child_tree = []
        if (rules(v)):
            traverse(v)
            if (len(child_tree) == 0):
                continue
            for child in child_tree:
                if (json['views'][child]['class'] == None):
                    continue
                if (json['views'][child]['class'] == 'android.webkit.WebView'):
                    is_ad_indices[child] = 1
                elif (json['views'][child]['class'] == 'android.widget.ImageView' or json['views'][child][
                    'class'] == 'android.widget.ViewFlipper' or 'qvhf.cbstp' in json['views'][child]['class'] or
                              json['views'][child]['class'] == 'com.qq.e.v2.plugin.n.c'):
                    if (check_position(json['views'][child])):
                        is_ad_indices[child] = 1
                        break
            break

    for i in range(len(json['views'])):
        # 如果view是web，判断大小。
        if (json['views'][i]['class'] == 'android.webkit.WebView'):
            web_size = json['views'][i]['size']
            wtemp_size = web_size.split('*')
            aw = int(wtemp_size[0])
            bw = int(wtemp_size[1])
            web_size = aw * bw
            if (web_size * 2 <= frame_size):
                is_ad_indices[i] = 1
    return is_ad_indices


def ad_picker4(json):
    is_ad_indices = [0] * len(json['views'])
    child_tree = []

    def rules(i):
        if json['views'][i]['class'] == None:
            return False
        if 'ad' in json['views'][i]['class'] and 'load' not in json['views'][i]['class'] and 'Load' not in \
                json['views'][i]['class'] and 'adapter' not in json['views'][i]['class'] and 'Head' not in \
                json['views'][i]['class'] and 'head' not in json['views'][i]['class'] and 'Radio' not in \
                json['views'][i]['class'] and 'road' not in json['views'][i]['class'] and 'adge' not in \
                json['views'][i]['class'] and 'shadow' not in json['views'][i]['class'] and 'pad' not in \
                json['views'][i]['class'] and 'adle' not in json['views'][i]['class']:
            return True
        if 'Ad' in json['views'][i]['class'] and 'Adapter' not in json['views'][i]['class']:
            return True
        if json['views'][i]['resource_id'] == None:
            return False
        if 'Ad' in json['views'][i]['resource_id'] and 'Adapter' not in json['views'][i]['class']:
            return True
        # if json['views'][i]['resource_id'] == 'id/0x1' and 'Layout' in json['views'][i]['class']:
        #     return True
        if 'id/0x8765' in json['views'][i]['resource_id'] and 'Layout' in json['views'][i]['class']:
            return True
        if 'id/ad' in json['views'][i]['resource_id'] and 'Layout' in json['views'][i]['class']:
            return True
        # if json['views'][i]['resource_id'] == 'id/content' and 'Layout' in json['views'][i]['class']:
        #     return True
        return False

    def traverse(root):
        child_list = json['views'][root]['children']
        if (len(child_list) == 0):
            return
        child_tree.extend(child_list)
        for child in child_list:
            traverse(child)

    def check_position(imageview):
        image_size = imageview['size']
        itemp_list = image_size.split('*')
        ai = int(itemp_list[0])
        bi = int(itemp_list[1])
        Iwidth = ai
        Iheight = bi
        image_size = ai * bi
        Ix1 = imageview['bounds'][0][0]
        Iy1 = imageview['bounds'][0][1]
        Ix2 = imageview['bounds'][1][0]
        Iy2 = imageview['bounds'][1][1]
        # 针对条型Image
        if (Iwidth >= fwidth * 0.9 and Iy2 < Frange1):
            return True
        elif (Iwidth >= fheight * 0.9 and Iy1 < Frange2):
            return True
        elif (Iwidth >= fwidth * 0.9 and Iy1 > Frange2):
            return True
        elif (Iwidth >= fheight * 0.9 and Iy1 > Frange2):
            return True
        # 针对中央型Image
        wdiv2 = Iwidth / 2
        hdiv2 = Iheight / 2
        Ictx = Ix1 + wdiv2
        Icty = Iy1 + hdiv2
        if (((Ictx - Fctx) ** 2 + (
                    Icty - Fcty) ** 2) ** 0.5 <= 100 and image_size * 13 >= frame_size and image_size * 1.5 <= 1920 * 1080):
            return True
        # 针对全屏型Image
        if (frame_size * 0.93 <= image_size and len(views_list) <= 2):
            return True
        return False

    def check_position_centre(imageview):
        image_size = imageview['size']
        itemp_list = image_size.split('*')
        ai = int(itemp_list[0])
        bi = int(itemp_list[1])
        Iwidth = ai
        Iheight = bi
        image_size = ai * bi
        Ix1 = imageview['bounds'][0][0]
        Iy1 = imageview['bounds'][0][1]
        Ix2 = imageview['bounds'][1][0]
        Iy2 = imageview['bounds'][1][1]
        # 针对中央型Image
        wdiv2 = Iwidth / 2
        hdiv2 = Iheight / 2
        Ictx = Ix1 + wdiv2
        Icty = Iy1 + hdiv2
        if (((Ictx - Fctx) ** 2 + (
                    Icty - Fcty) ** 2) ** 0.5 <= 100 and image_size * 13 >= frame_size and image_size * 1.5 <= 1920 * 1080):
            return True
        return False

    # webview判断
    views_list = []
    for i in range(1, len(json['views'])):
        if i not in views_list:
            views_list.append(json['views'][i]['class'])
    # 获取framesize,frame
    frame_size = json['views'][0]['size']
    ftemp_list = frame_size.split('*')
    a = int(ftemp_list[0])
    b = int(ftemp_list[1])
    fwidth = a
    fheight = b
    frame_size = a * b
    div3 = fheight / 3
    Fx1 = json['views'][0]['bounds'][0][0]
    Fy1 = json['views'][0]['bounds'][0][1]
    Fx2 = json['views'][0]['bounds'][1][0]
    Fy2 = json['views'][0]['bounds'][1][1]
    Frange1 = Fy1 + div3
    Frange2 = Fy1 + div3 * 2
    Fctx = Fx1 + fwidth / 2
    Fcty = Fy1 + fheight / 2

    for v in range(len(json['views'])):
        child_tree = []
        if (rules(v)):
            traverse(v)
            if (len(child_tree) == 0):
                continue
            for child in child_tree:
                if (json['views'][child]['class'] == None):
                    continue
                if (json['views'][child]['class'] == 'android.webkit.WebView'):
                    ws = json['views'][child]['size']
                    wtemp_size = ws.split('*')
                    a1 = int(wtemp_size[0])
                    a2 = int(wtemp_size[1])
                    ws = a1 * a2
                    if (ws > 0):
                        is_ad_indices[child] = 1
                elif (json['views'][child]['class'] == 'android.widget.ImageView' or json['views'][child][
                    'class'] == 'android.widget.ViewFlipper' or 'qvhf.cbstp' in json['views'][child]['class'] or
                              json['views'][child]['class'] == 'com.qq.e.v2.plugin.n.c' or 'AdWebView' in
                    json['views'][child]['class']):
                    if (check_position(json['views'][child])):
                        is_ad_indices[child] = 1

    for i in range(len(json['views'])):
        # 如果view是web，判断大小。
        if (json['views'][i]['class'] == 'android.webkit.WebView'):
            web_size = json['views'][i]['size']
            wtemp_size = web_size.split('*')
            aw = int(wtemp_size[0])
            bw = int(wtemp_size[1])
            web_size = aw * bw
            if (web_size * 2 <= frame_size and web_size > 0):
                is_ad_indices[i] = 1
        # ImageView
        if (json['views'][i]['class'] == 'android.widget.ImageView' or json['views'][i][
            'class'] == 'android.widget.ViewFlipper'):
            if (check_position_centre(json['views'][i])):
                is_ad_indices[i] = 1
        # other
        if (json['views'][i]['class'] != None):
            if ('Ad' in json['views'][i]['class'] or 'ad' in json['views'][i]['class']):
                if ('Load' not in json['views'][i]['class'] and 'load' not in json['views'][i][
                    'class'] and 'Adapter' not in
                    json['views'][i]['class'] and 'adapter' not in json['views'][i]['class'] and 'head' not in
                    json['views'][i]['class'] and 'Head' not in
                    json['views'][i]['class'] and 'Radio' not in json['views'][i]['class']):
                    if (check_position_centre(json['views'][i])):
                        is_ad_indices[i] = 1

    # filter
    filter_list = []
    for (vnum, isview) in enumerate(is_ad_indices):
        if isview == 1:
            Adx1 = json['views'][vnum]['bounds'][0][0]
            Ady1 = json['views'][vnum]['bounds'][0][1]
            Adx2 = json['views'][vnum]['bounds'][1][0]
            Ady2 = json['views'][vnum]['bounds'][1][1]
            loc_info = [Adx1, Ady1, Adx2, Ady2]
            if loc_info in filter_list:
                is_ad_indices[vnum] = 0
            else:
                filter_list.append(loc_info)

    if (ad_ex_by_traffic() == False):
        is_ad_indices = [0] * len(json['views'])

    return is_ad_indices


def ad_picker(json):
    # 对该页面中全部view的情况做统计
    views_list = []
    for i in range(1, len(json['views'])):
        if i not in views_list:
            views_list.append(json['views'][i]['class'])
    # 该页面中view是否是广告的标记，0不是，1是
    is_ad_indices = [0] * len(json['views'])
    # 获取framesize,frame
    frame_size = json['views'][0]['size']
    ftemp_list = frame_size.split('*')
    a = int(ftemp_list[0])
    b = int(ftemp_list[1])
    fwidth = a
    fheight = b
    frame_size = a * b
    div3 = fheight / 3
    Fx1 = json['views'][0]['bounds'][0][0]
    Fy1 = json['views'][0]['bounds'][0][1]
    Fx2 = json['views'][0]['bounds'][1][0]
    Fy2 = json['views'][0]['bounds'][1][1]
    Frange1 = Fy1 + div3
    Frange2 = Fy1 + div3 * 2
    Fctx = Fx1 + fwidth / 2
    Fcty = Fy1 + fheight / 2
    # print(Fctx, Fcty)
    # 遍历全部view
    for i in range(len(json['views'])):
        # 如果view是web，判断大小。
        if (json['views'][i]['class'] == 'android.webkit.WebView'):
            web_size = json['views'][i]['size']
            wtemp_size = web_size.split('*')
            aw = int(wtemp_size[0])
            bw = int(wtemp_size[1])
            web_size = aw * bw
            if (web_size * 2 <= frame_size):
                is_ad_indices[i] = 1
        # 如果是imageview，判断位置+大小。
        elif (json['views'][i]['class'] == 'android.widget.ImageView' or json['views'][i][
            'class'] == 'android.widget.ImageButton'):
            image_size = json['views'][i]['size']
            itemp_list = image_size.split('*')
            ai = int(itemp_list[0])
            bi = int(itemp_list[1])
            Iwidth = ai
            Iheight = bi
            image_size = ai * bi
            Ix1 = json['views'][i]['bounds'][0][0]
            Iy1 = json['views'][i]['bounds'][0][1]
            Ix2 = json['views'][i]['bounds'][1][0]
            Iy2 = json['views'][i]['bounds'][1][1]
            # 针对条型Image
            if (Iwidth >= fwidth * 0.9 and Iy2 < Frange1):
                is_ad_indices[i] = 1
            elif (Iwidth >= fwidth * 0.9 and Iy1 > Frange2):
                is_ad_indices[i] = 1
            # 针对中央型Image
            wdiv2 = Iwidth / 2
            hdiv2 = Iheight / 2
            Ictx = Ix1 + wdiv2
            Icty = Iy1 + hdiv2
            # print(Ictx, Icty)
            # print(((Ictx - Fctx) ** 2 + (Icty - Fcty) ** 2) ** 0.5)
            if (((Ictx - Fctx) ** 2 + (
                        Icty - Fcty) ** 2) ** 0.5 <= 50 and image_size * 13 >= frame_size and image_size * 2 <= frame_size):
                is_ad_indices[i] = 1
            # 针对全屏型Image
            if (frame_size * 0.93 <= image_size and len(views_list) <= 2):
                is_ad_indices[i] = 1
    return is_ad_indices


def is_overlap(jsonp, jsonn, relative_position, *views):
    def overlap(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
        if (Ax2 > Bx1 and Bx2 > Ax1 and Ay2 > By1 and By2 > Ay1):
            return True
        return False

    def check_views(views_num):
        for v in views:
            if (jsonn['views'][views_num]['class'] == v):
                return True
        return False

    view_indices_p = ad_picker4(jsonp)
    for (vnum, isview) in enumerate(view_indices_p):
        if isview == 1:
            Adx1 = jsonp['views'][vnum]['bounds'][0][0]
            Ady1 = jsonp['views'][vnum]['bounds'][0][1]
            Adx2 = jsonp['views'][vnum]['bounds'][1][0]
            Ady2 = jsonp['views'][vnum]['bounds'][1][1]
            Ad_size = jsonp['views'][vnum]['size']
            Adtemp_size = Ad_size.split('*')
            Adw1 = int(Adtemp_size[0])
            Adw2 = int(Adtemp_size[1])
            Ad_size = Adw1 * Adw2
            for i in range(len(jsonn['views'])):
                if (check_views(i)):
                    CBx1 = jsonn['views'][i]['bounds'][0][0]
                    CBy1 = jsonn['views'][i]['bounds'][0][1]
                    CBx2 = jsonn['views'][i]['bounds'][1][0]
                    CBy2 = jsonn['views'][i]['bounds'][1][1]
                    CB_size = jsonn['views'][i]['size']
                    CBtemp_size = CB_size.split('*')
                    CBw1 = int(CBtemp_size[0])
                    CBw2 = int(CBtemp_size[1])
                    CB_size = CBw1 * CBw2
                    # print (Adx1, Ady1, Adx2, Ady2, CBx1, CBy1, CBx2, CBy2)
                    if (relative_position == 0):
                        if (vnum > i and overlap(Adx1, Ady1, Adx2, Ady2, CBx1, CBy1, CBx2, CBy2)):
                            return True
                    elif (relative_position == 1):
                        # hidden + size
                        if (vnum < i and overlap(Adx1, Ady1, Adx2, Ady2, CBx1, CBy1, CBx2,
                                                 CBy2) and CB_size * 2 >= Ad_size):
                            return True
                    else:
                        if (overlap(Adx1, Ady1, Adx2, Ady2, CBx1, CBy1, CBx2, CBy2)):
                            return True
    return False


def tra(json, root):
    child_tree = []
    child_list = json['views'][root]['children']
    if (len(child_list) == 0):
        return
    child_tree.extend(child_list)
    for child in child_list:
        tra(child)
    return child_list


def check_by_rules(json_list):
    global json_tag_list
    fraud_mark_matrix = [[0 for col in range(len(json_list))] for row in range(type_count)]
    file_num = 0
    # 判断是否存在Installer
    installer_ext = 0
    for (tg, jsonfile) in json_dict.items():
        jsoni = json.loads(jsonfile)
        if (jsoni['foreground_activity'][
            0:jsoni['foreground_activity'].rfind('/',
                                                 1)] == 'com.android.packageinstaller'):
            installer_ext = 1
            break
    for (tg, jsonfile) in json_dict.items():
        json_tag_list.append(tg)
        json_content = json.loads(jsonfile)
        jsonp = json_content
        jsonn = json_content
        view_indices = ad_picker4(jsonp)
        print jsonp['tag'], view_indices
        # type 1: interaction fraud:insert ad control into interaction progress, such as dialog
        next = whoisnext(json_content['tag'])
        before = whoisbefore(json_content['tag'])
        if (before != None):
            before = json.loads(json_dict[before])
        # 找它的下个页面
        if (next != None):
            next_json = json.loads(json_dict[next])
            if (next_json['foreground_activity'][0:next_json['foreground_activity'].rfind('/', 1)] == main_activity):
                jsonn = next_json
            else:
                next2 = whoisnext(next_json['tag'])
                if (next2 != None):
                    next2_json = json.loads(json_dict[next2])
                    jsonn = next2_json

        ad_existence_n = 0
        for v in ad_picker4(jsonn):
            if v == 1:
                ad_existence_n = 1

        # 找切换的事件
        trans_content = json.loads(trans_file)
        for i in range(len(trans_content)):
            if (trans_content[i][1] == json_content['tag']):
                switch_event = trans_content[i][0]

        # print(is_overlap(jsonp, jsonn, 2, 'android.widget.Button'),is_overlap(jsonp, jsonn, 2,
        #                                                                         'android.widget.TextView'),ad_existence_n == 0,'BACK' not in
        #     switch_event,)
        # and jsonp['foreground_activity'] == jsonn['foreground_activity']
        if (is_overlap(jsonp, jsonn, 2, 'android.widget.TextView') and ad_existence_n == 0 and 'BACK' not in
            switch_event):
            fraud_mark_matrix[0][file_num] += 1

        # 对单个情况的添加
        # print(is_overlap(jsonp, jsonp, 2,'android.widget.TextView'))
        if (is_overlap(jsonp, jsonp, 2, 'android.widget.TextView') and is_overlap(jsonp, jsonp, 2,
                                                                                  'android.widget.Button')):
            fraud_mark_matrix[0][file_num] += 1
        if (fraud_mark_matrix[0][file_num] == 1 and before == None):
            fraud_mark_matrix[0][file_num] -= 1
            # fraud_mark_matrix[4][file_num] += 1
        elif (fraud_mark_matrix[0][file_num] == 1 and before['foreground_activity'][
                                                      0:before['foreground_activity'].rfind('/',
                                                                                            1)] != main_activity):
            fraud_mark_matrix[0][file_num] -= 1
            # fraud_mark_matrix[4][file_num] += 1
        # type 2: non-interaction fraud:download app without interaction with user
        ad_existence = 0
        adview_list = []
        adview_sizelist = []
        for v in view_indices:
            if v == 1:
                ad_existence = 1
        for k in range(0, len(view_indices)):
            if (view_indices[k] == 1):
                adview_list.append(jsonp['views'][k]['view_str'])
                adview_sizelist.append(jsonp['views'][k]['size'])
                # print adview_sizelist
        if 'current_traffic' not in json_content:
            if (next != None):
                # 下个页面直接安装应用+此页面有广告 2
                next_json = json.loads(json_dict[next])
                if (next_json['foreground_activity'][
                    0:next_json['foreground_activity'].rfind('/',
                                                             1)] == 'com.android.packageinstaller' and ad_existence == 1):
                    fraud_mark_matrix[1][file_num] += 5
                    # 下个页面没有弹出对话框 1
                if (is_in_views(next_json, 'android.widget.TextView') == False):
                    fraud_mark_matrix[1][file_num] += 1
                # 点击的是广告 1
                size_tt = 0
                trans_content = json.loads(trans_file)
                for i in range(len(trans_content)):
                    if (trans_content[i][1] == json_content['tag']):
                        trans_temp = trans_content[i][0]
                        size_tt = trans_temp[trans_temp.rfind('size') + 5:trans_temp.rfind('text') - 1]
                click_ad = 0
                for k in adview_sizelist:
                    if (size_tt == k):
                        click_ad = 1
                if (click_ad == 1):
                    fraud_mark_matrix[1][file_num] += 1
                # 下个页面应当是程序内页面，外面不算
                if (next_json['foreground_activity'][
                    0:json_content['foreground_activity'].rfind('/', 1)] == main_activity):
                    fraud_mark_matrix[1][file_num] += 1
                # 下个页面的view_str应当相同
                # if (jsonp['foreground_activity'] == next_json['foreground_activity']):
                #     fraud_mark_matrix[1][file_num] += 1
                # 剩余页面中存在installer
                if (installer_ext == 1):
                    fraud_mark_matrix[1][file_num] += 2
                # 检查当前界面是否存在广告
                if (ad_existence == 0):
                    fraud_mark_matrix[1][file_num] -= 1
        else:
            # type 2 for new
            if (next != None):
                next_json = json.loads(json_dict[next])
                if (next_json['foreground_activity'][
                    0:next_json['foreground_activity'].rfind('/',
                                                             1)] == 'com.android.packageinstaller' and ad_existence == 1):
                    fraud_mark_matrix[1][file_num] += 5
            # calc the trafic
            jsonp_time = int(jsonp['tag'][jsonp['tag'].rfind('_') + 1:])
            jsonp_traffic = int(jsonp['current_traffic'])
            json2 = whoisnext(jsonp['tag'])
            if json2 != None:
                json2 = json.loads(json_dict[next])
                json2_time = int(json2['tag'][jsonp['tag'].rfind('_') + 1:])
                json2_traffic = int(json2['current_traffic'])
                speed = (json2_traffic - jsonp_traffic) / (json2_time - jsonp_time)
                # print speed
            else:
                speed = 0
            # ad_existence
            # click the ad
            trans_content = json.loads(trans_file)
            size_tt = 0
            for i in range(len(trans_content)):
                if (trans_content[i][1] == json_content['tag']):
                    trans_temp = trans_content[i][0]
                    size_tt = trans_temp[trans_temp.rfind('size') + 5:trans_temp.rfind('text') - 1]
            click_ad = 0
            for k in adview_sizelist:
                if (size_tt == k):
                    click_ad = 1
            if (speed / 1000 >= 50 and ad_existence == 1 and click_ad == 1):
                fraud_mark_matrix[1][file_num] += 5
        # type 3: hidden fraud: hidden ad control under orther cotrol
        if (is_overlap(jsonp, jsonp, 1, 'android.widget.Button', 'android.widget.ImageButton',
                       'android.support.design.widget.FloatingActionButton', 'com.androidemu.EmulatorView2')):
            fraud_mark_matrix[2][file_num] += 1
        # type 4: too small or too large or outside screen
        frame_size = json_content['views'][0]['size']
        ftemp_list = frame_size.split('*')
        a = int(ftemp_list[0])
        b = int(ftemp_list[1])
        frame_size = a * b
        max = 0
        min = 0
        maxsize = 0
        minsize = frame_size
        # 获取最大，最小的广告
        for (i, v) in enumerate(view_indices):
            if v == 1:
                size = json_content['views'][i]['size']
                temp_list = size.split('*')
                a = int(temp_list[0])
                b = int(temp_list[1])
                size = a * b
                if size > maxsize:
                    maxsize = size
                    max = i
                if size < minsize:
                    minsize = size
                    min = i
        # 判定尺寸
        if (minsize > 0 and maxsize > 0 and maxsize < frame_size * 10):
            if (maxsize > frame_size + 3 or 0 < minsize <= frame_size / 50):
                # print(maxsize, minsize)
                fraud_mark_matrix[3][file_num] += 1
        # type 5: overlap fraud: an ad control partially covers a clickable non-ad control
        if (is_overlap(jsonp, jsonp, 0, 'android.widget.Button', 'android.widget.ImageButton',
                       'android.support.design.widget.FloatingActionButton')):
            fraud_mark_matrix[4][file_num] += 1
        # type 6: number fraud: the number of viewable ads in a screen is more than k, the maximum allowed number of ads
        ad_count = 0
        adType_list = []
        for (c, v) in enumerate(view_indices):
            if v == 1:
                ad_count += 1
                adType_list.append(jsonp['views'][c]['class'])
        if (ad_count >= 3 and jsonp['foreground_activity'][
                              0:json_content['foreground_activity'].rfind('/', 1)] == main_activity):
            fraud_mark_matrix[5][file_num] += 1
        # if (len(adType_list) == 3 and adType_list[0] == adType_list[0] == adType_list[0] == 'android.widget.ImageView'):
        #     fraud_mark_matrix[5][file_num] -= 1
        # type 7: pop-window fraud: pop window in no-own activity
        if (json_content['foreground_activity'][
            0:json_content['foreground_activity'].rfind('/', 1)] != main_activity and json_content[
                                                                                          'foreground_activity'][
                                                                                      0:json_content[
                                                                                          'foreground_activity'].rfind(
                                                                                          '/',
                                                                                          1)] != 'com.android.systemui' and
                    json_content[
                        'foreground_activity'][
                    0:json_content[
                        'foreground_activity'].rfind(
                        '/',
                        1)] != 'com.android.dialer' and ad_existence == 1):
            fraud_mark_matrix[6][file_num] += 1
        file_num += 1
    # print(main_activity)
    result = output_result(fraud_mark_matrix)
    return result


def check(p):
    global path, trans_path, filepath, output_path
    global activity_dict, main_activity, json_dict, json_tag_list, trans_file
    trans_file = ''
    activity_dict = {}
    main_activity = 'null'
    json_dict = {}
    json_tag_list = []
    if (str(p).rfind(sep, 1) != len(p) - 1):
        print("Path format error !")
    else:
        path = p
        temp = str(path)
        trans_path = path + 'state_transitions.json'
        filepath = path + 'states'
        if (os.path.exists(trans_path) == False or os.path.exists(filepath) == False):
            return False
        output_path = temp.replace(path[path.rfind(sep, 1, len(path) - 1) + 1:path.rfind(sep, 1)], 'out')
        read_files()
        get_activity(json_dict)
        result = check_by_rules(json_dict)
        return result

# check('D:\\PaperW\\Stage2\\for_zsd_20170411\\eb45cc2643307097ca95ee83a4f9ebb1\\')



# if (len(sys.argv) == 1):
#     print("No path !")
# elif (str(sys.argv[1]).rfind('\\', 1) != len(sys.argv[1]) - 1):
#     print("Path format error !")
# else:
#     path = sys.argv[1]
#     temp = str(path)
#     trans_path = path + 'state_transitions.json'
#     filepath = path + 'states'
#     output_path = temp.replace(path[path.rfind("\\", 1, len(path) - 1) + 1:path.rfind("\\", 1)], 'out')
#     read_files()
#     get_activity(json_dict)
#     check_by_rules(json_dict)

# read_files()
# get_activity(json_dict)
# check_by_rules(json_dict)
