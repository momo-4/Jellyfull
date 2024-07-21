import tkinter as tk
from tkinter import filedialog

import maker
import retriever


def main():
    mode_ = input(
        "请输入媒体的类型:\n"
        "1 - 电影\n2 - 连续剧\n3 - 电视单季\n")
    match mode_:
        case "1":
            mode_ = 'movie'
        case "2":
            mode_ = 'tvshow'
        case "3":
            mode_ = 'season'
        case _:
            raise ValueError(f"Mode {mode_} is not supported.")
    url = input("请输入需要刮削的电影或剧集的网址^u^ \n（支持豆瓣、IGDB、IMDB、TMDB、Bangumi等链接）\n")

    r = retriever.NeoDBRetriever()
    retrieve_st = r.retrieve_from_url(url)
    retrieve_nd = r.retrieve_from_uuid(mode=retrieve_st['category'], uuid=retrieve_st['uuid'])

    _ = input('回车后选择需要刮削的电影文件或电视剧文件夹路径（Jellyfull会启动文件系统窗口）\n')

    root = tk.Tk()
    root.withdraw()
    if mode_ == 'movie':
        file = filedialog.askopenfilename()
    elif mode_ == 'tvshow' or mode_ == 'season':
        file = filedialog.askdirectory()
    else:
        raise ValueError(f"Mode {mode_} is not supported.")

    m = maker.NfoMaker(file)
    print(f"处理地址为 {file}")
    m.parse_from_neodb(data=retrieve_nd, mode=mode_)
    m.make()
    m.save()
    print(f"成功创建NFO文件")


if __name__ == '__main__':
    main()
