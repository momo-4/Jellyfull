# Jellyfull - 适用于Jellyfin的媒体元数据刮削工具
Jellyfull是一个用于Jellyfin的媒体元数据刮削工具，它可以从豆瓣、TMDB、TVDB、IMDB、Bangumi等网站获取电影、电视剧、动漫等媒体的元数据信息，并将其保存到Jellyfin的数据库中。
Jellyfull目前只适用于简体中文环境，未来可能会支持更多语言。

## 安装
```cmd
git clone <the github repository>
cd /<your disk>/jellyfull
pip install poetry
poetry update
```

## 用法
### 交互式
```cmd
python jellyfull.py
> 请输入媒体的类型:
1 - 电影
2 - 连续剧
3 - 电视单季
2

> 请输入需要刮削的电影或剧集的网址^u^
  （支持豆瓣、IGDB、IMDB、TMDB、Bangumi等链接）
https://movie.douban.com/subject/30291583/

>回车后选择需要刮削的电影文件或电视剧文件夹路径（Jellyfull会启动文件系统窗口）
  <假装你选择了 D:/我们由奇迹构成/>  
  
处理地址为 D:/我们由奇迹构成/
成功创建NFO文件
```
### 直接调用模组
```python
from jellyfull import retriever, maker

r = retriever.NeoDBRetriever()
r1 = r.retrieve_from_url('https://movie.douban.com/subject/30291583/')
r2 = r.retrieve_from_uuid(mode='tv', uuid=r1['uuid'])

m = maker.NfoMaker(r'D:/我们由奇迹构成/')
m.parse_from_neodb(data=r2, mode='tvshow')
m.make()
m.save()
```

## Jellyfull没有什么功能
- jellyfull不会自动刮削，需要手动输入网址，通过人脑代替文本识别
- jellyfull不支持批量刮削

## FAQ
#### 为什么要在有众多竞品的情况下开发Jellyfull？
- 精确的说，Jellyfull并不是一个竞品，它只是一个简单的工具，用于解决Jellyfin在中文环境下的元数据刮削问题，毕竟在Jellyfin手动添加元数据挺累的。
- 不是所有人都背靠一个巨大的媒体库，其他工具试图解决大量数据的识别问题，而Jellyfull更在乎如何获得精确的元数据，故而尝试通过人脑代替机器识别（从媒体的公开网址出发）。
- 如果你是家庭用户或者想和你的朋友分享一些你感兴趣的媒体，那么Jellyfull可能是一个不错的选择。
#### 为什么要分成连续剧和电视单季？
Jellyfin的元数据模型中，连续剧和电视单季是两种不同的类型，元数据会分别读取`tvshow.nfo`和`season.nfo`，因此需要分开处理。
#### Jellyfull如何支持公开网址的刮削？
- Jellyfull使用了NeoDB的API，通过网址获取媒体的UUID，再通过UUID获取媒体的元数据信息。
- NeoDB是一个开源项目和免费服务，旨在帮助用户管理、共享和发现 Fediverse 中文化产品（例如书籍、电影、音乐、播客、游戏和表演）的收藏、评论和评级。
更多信息请关注neodb@mastodon.social
## 致谢
- [Jellyfin](https://github.com/jellyfin/jellyfin)
- [NeoDB](https://github.com/neodb-social/neodb)

## License
Apache-2.0
