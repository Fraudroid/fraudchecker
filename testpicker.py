# encoding:utf-8
import json
import os

type_count = 8
# path = 'D:\\PaperW\\Stage2\\data\\tjmusic\\'
# path = 'D:\\PaperW\\Stage2\\data\\2017_01_10\\2017_01_10\\overlap\\'
path = ''
output_path = ''
trans_path = ''
filepath = ''
activity_dict = {}
main_activity = 'null'
json_dict = {}
json_tag_list = []
trans_file = ''
sep = os.path.sep


def read_files():
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s//%s' % (filepath, allDir))
        if (child.endswith('json')):
            f = open(child)
            jsonfile = f.read()
            json_content = json.loads(jsonfile)
            json_dict[json_content['tag']] = jsonfile


def ad_picker2(json):
    # 根据resource_id或者class的内容判断是否是广告+webview判断
    is_ad_indices = [0] * len(json['views'])
    for i in range(len(json['views'])):
        if 'ad' in json['views'][i]['class'] or 'Ad' in json['views'][i]['class']:
            is_ad_indices[i] = 1
        if 'ad' in json['views'][i]['class'] or 'Ad' in json['views'][i]['resource_id'] or '0x1' in json['views'][i][
            'resource_id']:
            is_ad_indices[i] = 1
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
    return is_ad_indices


def traverse(json, root):
    child_list = json['views'][root]['children']
    if (len(child_list) == 0):
        return
    child_tree.extend(child_list)
    for child in child_list:
        traverse(json, child)


def ad_picker3(json):
    is_ad_indices = [0] * len(json['views'])
    child_tree = []

    def rules(i):
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
            # print frame_size,image_size
            if (((Ictx - Fctx) ** 2 + (
                        Icty - Fcty) ** 2) ** 0.5 <= 50 and image_size * 13 >= frame_size and image_size * 2 <= frame_size):
                is_ad_indices[i] = 1
            # 针对全屏型Image
            if (frame_size * 0.93 <= image_size and len(views_list) <= 2):
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
                json['views'][i]['class']:
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
                    Icty - Fcty) ** 2) ** 0.5 <= 100 and image_size * 13 >= frame_size and image_size * 1.5 <= frame_size):
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
        print frame_size,image_size
        print(((Ictx - Fctx) ** 2 + (
                    Icty - Fcty) ** 2) ** 0.5)
        if (((Ictx - Fctx) ** 2 + (
                    Icty - Fcty) ** 2) ** 0.5 <= 100 and image_size * 13 >= frame_size and image_size * 1.5 <= 1920*1080):
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

    return is_ad_indices


child_tree = []
filepath = 'D:\\PaperWork\\Stage2\\gt\\2fc0fb394d9e685256844e3f1638a1fb\\state\\'
read_files()
for (tg, jsonfile) in json_dict.items():
    json_tag_list.append(tg)
    json_content = json.loads(jsonfile)
    jsonp = json_content
    print tg, ad_picker4(jsonp)
