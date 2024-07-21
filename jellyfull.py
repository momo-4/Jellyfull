import tkinter as tk
from tkinter import filedialog

import maker
import retriever


def main():
    mode_ = input("请输入媒体的类型 \n（仅支持输入电影、连续剧或电视单季）\n")
    match mode_:
        case '电影':
            mode_ = 'movie'
        case '连续剧':
            mode_ = 'tvshow'
        case '电视单季':
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

    file = filedialog.askdirectory()

    m = maker.NfoMaker(file)
    print(f"处理地址为 {file}")
    m.parse_from_neodb(data=retrieve_nd, mode=mode_)
    m.make()
    m.save()
    print(f"成功创建NFO文件")


if __name__ == '__main__':
    main()
