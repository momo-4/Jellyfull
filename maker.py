import os
import time


class NfoMaker:
    def __init__(self, file: str):
        self._template = {
            'movie': {
                'mode': 'movie',
                'folder': os.path.abspath(os.path.dirname(file)),
                'file_name': os.path.splitext(os.path.basename(os.path.abspath(file)))[0],
                'plot': None,
                'lockdata': 'true',
                'dateadded': None,
                'title': None,
                'originaltitle': None,
                'sorttitle': [],
                'director': [],
                'writer': [],
                'rating': None,
                'year': None,
                'premiered': None,
                'releasedate': None,
                'genre': [],
                'tag': [],
                'actors': [],
                'imdbid': None,
            },
            'tvshow': {
                'mode': 'tvshow',
                'folder': os.path.abspath(file),
                'file_name': 'tvshow',
                'plot': None,
                'lockdata': 'true',
                'dateadded': None,
                'title': None,
                'originaltitle': None,
                'sorttitle': [],
                'director': [],
                'writer': [],
                'rating': None,
                'year': None,
                'premiered': None,
                'releasedate': None,
                'genre': [],
                'tag': [],
                'actors': [],
                'imdbid': None,
                'season': '-1',
                'episode': '-1',
            },
            'season': {
                'mode': 'season',
                'folder': os.path.abspath(file),
                'file_name': 'season',
                'plot': None,
                'lockdata': 'true',
                'dateadded': None,
                'title': None,
                'originaltitle': None,
                'sorttitle': [],
                'director': [],
                'writer': [],
                'rating': None,
                'year': None,
                'premiered': None,
                'releasedate': None,
                'genre': [],
                'tag': [],
                'actors': [],
                'imdbid': None,
                'seasonnumber': None,
                'episode': '-1',
            },

        }
        self.metadata = None
        self.nfo = None

    def parse_from_neodb(self, data: dict, mode: str):
        if mode not in self._template:
            raise ValueError(f"Mode {mode} is not supported.")

        meta_data = self._template[mode]
        meta_data['plot'] = data['description']
        meta_data['dateadded'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        meta_data['title'] = data['title']
        meta_data['originaltitle'] = data['orig_title']
        meta_data['sorttitle'] = ' / '.join([i['text'] for i in data['localized_title']])
        meta_data['director'] = data['director']
        meta_data['writer'] = data['playwright']
        meta_data['rating'] = data['rating']
        meta_data['year'] = str(data['year'])
        meta_data['premiered'] = str(data['year']) + '-01-01'
        meta_data['releasedate'] = str(data['year']) + '-01-01'
        meta_data['tag'] = data['language']
        meta_data['actors'] = data['actor']
        try:
            meta_data['imdbid'] = data['imdb']
        except KeyError:
            pass
        for genre in data['genre']:
            genre = self._convert_genre(genre)
            if genre is not None:
                meta_data['genre'].append(genre)

        if mode == 'season':
            meta_data['seasonnumber'] = str(data['season_number'])

        self.metadata = meta_data

        return self.metadata

    def make(self):
        if self.metadata is None:
            raise ValueError("No metadata found.")
        data = self.metadata
        nfo = '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n'
        nfo += f'<{data["mode"]}>\n'
        nfo += f'  <plot>{data["plot"]}</plot>\n'
        nfo += f'  <lockdata>{data["lockdata"]}</lockdata>\n'
        nfo += f'  <dateadded>{data["dateadded"]}</dateadded>\n'
        nfo += f'  <title>{data["title"]}</title>\n'
        nfo += f'  <originaltitle>{data["originaltitle"]}</originaltitle>\n'
        nfo += f'  <sorttitle>{data["sorttitle"]}</sorttitle>\n'
        for director in data["director"]:
            nfo += f'  <director>{director}</director>\n'
        for writer in data["writer"]:
            nfo += f'  <writer>{writer}</writer>\n'
            nfo += f'  <credits>{writer}</credits>\n'
        nfo += f'  <rating>{data["rating"]}</rating>\n'
        nfo += f'  <year>{data["year"]}</year>\n'
        nfo += f'  <premiered>{data["premiered"]}</premiered>\n'
        nfo += f'  <releasedate>{data["releasedate"]}</releasedate>\n'
        for genre in data["genre"]:
            nfo += f'  <genre>{genre}</genre>\n'
        for tag in data["tag"]:
            nfo += f'  <tag>{tag}</tag>\n'
        for actor in data["actors"]:
            nfo += '  <actor>\n'
            nfo += f'    <name>{actor}</name>\n'
            nfo += '    <type>Actor</type>\n'
            nfo += '  </actor>\n'
        if data["imdbid"] is not None:
            nfo += f'  <imdbid>{data["imdbid"]}</imdbid>\n'
        if data["mode"] == 'season':
            nfo += f'  <seasonnumber>{data["seasonnumber"]}</seasonnumber>\n'
        nfo += f'</{data["mode"]}>\n'

        self.nfo = nfo
        return self.nfo

    def save(self):
        if self.nfo is None:
            raise ValueError("No nfo found.")
        with open(os.path.join(self.metadata['folder'], self.metadata['file_name'] + '.nfo'),
                  mode='w',
                  encoding='utf-8') as f:
            f.write(self.nfo)

    @staticmethod
    def _convert_genre(genre):
        match genre:
            case 'Drama':
                genre = '剧情'
            case 'Romance':
                genre = '爱情'
            case 'Comedy':
                genre = '喜剧'
            case 'Action':
                genre = '动作'
            case 'Thriller':
                genre = '惊悚'
            case 'Horror':
                genre = '恐怖'
            case 'Crime':
                genre = '犯罪'
            case 'Adventure':
                genre = '冒险'
            case 'Science Fiction':
                genre = '科幻'
            case 'Fantasy':
                genre = '奇幻'
            case 'Mystery':
                genre = '悬疑'
            case 'Family':
                genre = '家庭'
            case 'Animation':
                genre = '动画'
            case 'Music':
                genre = '音乐'
            case 'History':
                genre = '历史'
            case 'War':
                genre = '战争'
            case 'Documentary':
                genre = '纪录'
            case 'Western':
                genre = '西部'
            case 'TV Movie':
                genre = '电视电影'
            case 'Biography':
                genre = '传记'
            case 'Sport':
                genre = '体育'
            case 'Musical':
                genre = '音乐剧'
            case _:
                return None
        return genre

