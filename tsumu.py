import cv2
import numpy as np
import math

def resize(img):
    # resize window
    screen_res = 1280, 720
    scale_width = screen_res[0] / img.shape[1]
    scale_height = screen_res[1] / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    return window_width, window_height

# 中心周辺の色を平均可してツムを色にする
def averageColor(crop, ancestor):
    # RGB平均値を出力
    # flattenで一次元化しmeanで平均を取得 
    b = crop.T[0].flatten().mean()
    g = crop.T[1].flatten().mean()
    r = crop.T[2].flatten().mean()

    if b == "nan" or g == "nan" or r == "nan":
        b = 255
        g = 255
        r = 255
    
    # ダサすぎる
    if b <= 64:
        b = 25
    elif 64 < b <= 128:
        b = 75
    elif 128 < b <=192:
        b = 125
    elif 192 < b <=255:
        b = 170
    
    if g <= 64:
        g = 25
    elif 64 < g <= 128:
        g = 75
    elif 128 < g <=192:
        g = 125
    elif 192 < g <=255:
        g = 170

    if r <= 64:
        r = 32
    elif 64 < r <= 128:
        r = 96
    elif 128 < r <=192:
        r = 160
    elif 192 < r <=255:
        r = 224

    color = {
        "blue": b,
        "green": g,
        "red":r
    }
    return color

# ダブりを消す処理
def get_unique_list(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

def main():
    # TODO 処理の最初でスクショを取得する
    # 取得したスクショをいじる
    img = cv2.imread('./img/tumu.jpg',0)
    color_img = cv2.imread('./img/tumu.jpg')
    ancestor = cv2.imread('./img/tumu.jpg')
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    a = 4
    image = cimg
    lut = [ np.uint8(255.0 / (1 + math.exp(-a * (i - 128.) / 255.))) for i in range(256)] 
    result_image = np.array( [ lut[value] for value in image.flat], dtype=np.uint8 )
    cimg = result_image.reshape(image.shape)
    
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,param1=65,param2=28,minRadius=67,maxRadius=130)
    circles = np.uint16(np.around(circles))
    center_list = []
    for i in circles[0,:]:
        # draw the outer circle 
        # color version
        # 円は色分けの範囲より大きめにする
        circle_size = math.floor(i[2]*1.35)
        cv2.circle(color_img,(i[0],i[1]),circle_size,(0,255,0),8)
        # draw the center of the circle
        cv2.circle(color_img,(i[0],i[1]),2,(0,0,255),7)
        # 中心周辺の色を取得する
        crop = ancestor[i[1]-30:i[1]+30, i[0]-30:i[0]+30]
        color = averageColor(crop, ancestor)

        center_list.append({
            "color": color,
            "center_x": i[0],
            "center_y": i[1],
        })

    all_list = []
    for k in center_list:
        cv2.circle(
            color_img,
            (k["center_x"], k["center_y"]),
            100,
            (k["color"]["blue"], k["color"]["green"], k["color"]["red"]),
            -1
        )
        # 色の種類
        all_list.append(
            {
            "blue": k["color"]["blue"],
            "green": k["color"]["green"],
            "red": k["color"]["red"]
            }
        )

    color_list = get_unique_list(all_list)
    print(len(color_list))

    # TODO center_list rename cercle_info
    # 色ごとにグループ化
    group = []
    index = 0
    for i in color_list:
        sub = []
        for j in center_list:
            if i["blue"] == j["color"]["blue"] and i["green"] == j["color"]["green"] and i["red"] == j["color"]["red"]:
                sub.append(j)
        group.append(sub)
        
        index += 1

    print(len(group))
    print(len(group[3]))
    print(group)



    # TODO 同じ色で、円が3つ以上重なっている箇所を検知する
    # TODO 検知した3つ以上の円の中心点を取得する。
    # ここからPCのカーソルを操作する
    # TODO 中心点を繋ぐ処理　

    ############# Debug    
    size = resize(color_img)
    cv2.namedWindow('color', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('color', size[0], size[1])
    cv2.imshow('color',color_img)
    ############# Debug END

    # end process
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()