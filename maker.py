import os
import time
import xml.etree.ElementTree as ET


def _load_language_map():
    rows = open(os.path.join(os.path.dirname(__file__), "iso639-1.tsv"), encoding="utf-8").read().splitlines()[1:]
    return {r[0].lower(): r[1] for line in rows if len(r := line.split("\t", 2)) >= 2 and r[1] not in ("", "-")}


class NfoMaker:
    _language_map: dict[str, str] = _load_language_map()
    _GENRE_MAP: dict[str, str] = {
        "Drama": "剧情", "Romance": "爱情", "Comedy": "喜剧",
        "Action": "动作", "Thriller": "惊悚", "Horror": "恐怖",
        "Crime": "犯罪", "Adventure": "冒险", "Science Fiction": "科幻",
        "Fantasy": "奇幻", "Mystery": "悬疑", "Family": "家庭",
        "Animation": "动画", "Music": "音乐", "History": "历史",
        "War": "战争", "Documentary": "纪录", "Western": "西部",
        "TV Movie": "电视电影", "Biography": "传记", "Sport": "体育",
        "Musical": "音乐剧",
    }

    def __init__(self, file: str):
        self._file = file
        self.metadata = None
        self.nfo = None

    def parse_from_neodb(self, data: dict, mode: str):
        _VALID_MODES = {"movie", "tvshow", "season"}
        if mode not in _VALID_MODES:
            raise ValueError(f"Mode {mode} is not supported.")

        file = self._file
        if mode == "movie":
            folder = os.path.abspath(os.path.dirname(file))
            file_name = os.path.splitext(os.path.basename(os.path.abspath(file)))[0]
        else:
            folder = os.path.abspath(file)
            file_name = mode

        year = str(data["year"])
        meta_data = {
            "mode": mode,
            "folder": folder,
            "file_name": file_name,
            "plot": data["description"],
            "lockdata": "true",
            "dateadded": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "title": data["title"],
            "originaltitle": data["orig_title"],
            "sorttitle": " / ".join(i["text"] for i in data["localized_title"]),
            "director": data["director"],
            "writer": data["playwright"],
            "rating": data["rating"],
            "year": year,
            "premiered": year + "-01-01",
            "releasedate": year + "-01-01",
            "genre": [cn for g in data["genre"] if (cn := self._convert_genre(g)) is not None],
            "tag": [self._language_map.get(lang.strip().lower(), lang) for lang in data.get("language", [])],
            "actors": data["actor"],
            "imdbid": data.get("imdb"),
        }

        if mode == "tvshow":
            meta_data["season"] = "-1"
            meta_data["episode"] = "-1"
        elif mode == "season":
            meta_data["seasonnumber"] = str(data["season_number"]) if "season_number" in data else None
            meta_data["episode"] = "-1"

        self.metadata = meta_data
        return self.metadata

    def make(self):
        if self.metadata is None:
            raise ValueError("No metadata found.")
        data = self.metadata
        root = ET.Element(data["mode"])

        ET.SubElement(root, "plot").text = data["plot"]
        ET.SubElement(root, "lockdata").text = data["lockdata"]
        ET.SubElement(root, "dateadded").text = data["dateadded"]
        ET.SubElement(root, "title").text = data["title"]
        ET.SubElement(root, "originaltitle").text = data["originaltitle"]
        ET.SubElement(root, "year").text = data["year"]
        ET.SubElement(root, "sorttitle").text = data["sorttitle"]
        if data["imdbid"] is not None:
            ET.SubElement(root, "imdbid").text = data["imdbid"]
        ET.SubElement(root, "premiered").text = data["premiered"]
        ET.SubElement(root, "releasedate").text = data["releasedate"]
        for genre in data["genre"]:
            ET.SubElement(root, "genre").text = genre
        for tag in data["tag"]:
            ET.SubElement(root, "tag").text = tag
        for director in data["director"]:
            ET.SubElement(root, "director").text = director
        for writer in data["writer"]:
            ET.SubElement(root, "writer").text = writer
            ET.SubElement(root, "credits").text = writer
        ET.SubElement(root, "rating").text = str(data["rating"])
        for actor in data["actors"]:
            actor_el = ET.SubElement(root, "actor")
            ET.SubElement(actor_el, "name").text = actor
            ET.SubElement(actor_el, "type").text = "Actor"

        if data["mode"] == "season" and data["seasonnumber"] is not None:
            ET.SubElement(root, "seasonnumber").text = data["seasonnumber"]

        ET.indent(root, space="  ")
        self.nfo = '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n' + ET.tostring(root, encoding="unicode") + "\n"
        return self.nfo

    def save(self):
        if self.nfo is None:
            raise ValueError("No nfo found.")
        with open(
            os.path.join(self.metadata["folder"], self.metadata["file_name"] + ".nfo"),
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(self.nfo)

    @classmethod
    def _convert_genre(cls, genre: str) -> str | None:
        return cls._GENRE_MAP.get(genre)


