"""Populate the database with an assortment of information."""

import dataclasses
import logging
import typing as t

import requests

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclasses.dataclass(frozen=True)
class Resource:
    """A described resource."""

    name: str
    attrs: t.Sequence[str]

    @property
    def others(self) -> t.Sequence[str]:
        """Everything except first attr."""
        return self.attrs[1:]

    @property
    def key(self) -> str:
        """First attr."""
        return self.attrs[0]


DataStructure = t.Tuple[Resource, t.Sequence[t.Sequence[object]]]

mood: DataStructure = (
    Resource("moods", []),
    [
        ["Relaxed"],
        ["Focused"],
        ["Intense"],
        ["Vibrant"],
        ["Sensual"],
        ["Somber"],
        ["Zany"],
        ["Content"],
        ["Joyful"],
    ],
)

color: DataStructure = (
    Resource("colors", ["hue", "saturation", "brightness"]),
    [
        ["Crimson Red", 0, 100, 30],
        ["Midnight Blue", 240, 100, 40],
        ["Forest Green", 120, 100, 40],
        ["Royal Purple", 280, 100, 60],
        ["Sky Blue", 204, 100, 100],
        ["Chartreuse Green", 80, 60, 100],
        ["Sunshine Yellow", 60, 100, 100],
        ["Magenta", 324, 100, 100],
        ["Tangerine Orange", 36, 100, 100],
        ["Rose Pink", 320, 60, 100],
        ["Soft Green", 120, 20, 100],
        ["Lavendar Purple", 270, 40, 100],
        ["Ducky Yellow", 60, 40, 100],
    ],
)

shape: DataStructure = (
    Resource("shapes", ["sides"]),
    [
        ["Square", 4],
        ["Triangle", 3],
        ["Circle", 1],
        ["Rectangle", 4],
        ["Pentagon", 5],
        ["Hexagon", 6],
        ["Star", 10],
        ["Diamond", 4],
        ["Oval", 1],
    ],
)

scent: DataStructure = (
    Resource("scents", ["family"]),
    [
        ["Floral", "Floral"],
        ["Fruity", "Floral and Fresh"],
        ["Citrus", "Fresh"],
        ["Tropical", "Fresh and Oriental"],
        ["Earthy", "Woody"],
        ["Herbal", "Fresh and Woody"],
        ["Musk", "Woody"],
        ["Fresh", "Fresh"],
        ["Spice", "Oriental"],
    ],
)

taste: DataStructure = (
    Resource("tastes", []),
    [
        ["Sweet"],
        ["Sour"],
        ["Salty"],
        ["Bitter"],
        ["Spicy"],
        ["Umami"],
    ],
)

music: DataStructure = (
    Resource("musics", []),
    [
        ["Pop"],
        ["Rhythm and Blues"],
        ["Rap"],
        ["Hip hop"],
        ["Rock"],
        ["Classical"],
        ["Jazz"],
        ["Country"],
        ["Folk"],
        ["Metal"],
        ["EDM"],
        ["Hyperpop"],
    ],
)

media: DataStructure = (
    Resource("medias", []),
    [
        ["Fantasy"],
        ["Action"],
        ["Horror"],
        ["Science Fiction"],
        ["Historical Fiction"],
        ["Documentary"],
        ["Drama"],
        ["Comedy"],
        ["Tragedy"],
        ["Thriller"],
        ["Musical"],
        ["Romance"],
    ],
)

connections = (
    Resource("connections", ["color", "scent", "taste", "shape", "media", "music"]),
    [
        [
            "Relaxed",
            "Lavendar Purple",
            "Herbal",
            "Sweet",
            "Oval",
            "Historical Fiction",
            "Classical",
        ],
        [
            "Focused",
            "Midnight Blue",
            "Fresh",
            "Salty",
            "Rectangle",
            "Documentary",
            "Rhythm and Blues",
        ],
        [
            "Intense",
            "Crimson Red",
            "Spice",
            "Sour",
            "Hexagon",
            "Thriller",
            "Rap",
        ],
        [
            "Vibrant",
            "Tangerine Orange",
            "Tropical",
            "Sour",
            "Square",
            "Action",
            "Rock",
        ],
        [
            "Sensual",
            "Magenta",
            "Floral",
            "Citrus",
            "Diamond",
            "Romance",
            "Jazz",
        ],
        [
            "Somber",
            "Forest Green",
            "Musk",
            "Bitter",
            "Pentagon",
            "Tragedy",
            "Classical",
        ],
        [
            "Zany",
            "Chartreuse",
            "Fruity",
            "Spicy",
            "Star",
            "Comedy",
            "Hyperpop",
        ],
        [
            "Content",
            "Sky Blue",
            "Woody",
            "Umami",
            "Circle",
            "Musical",
            "Folk",
        ],
        [
            "Joyful",
            "Sunshine Yellow",
            "Citrus",
            "Salty",
            "Triangle",
            "Comedy",
            "Pop",
        ],
    ],
)


def populate() -> None:
    """Actually hit the endpoints to populate the data."""
    all_data: t.Sequence[DataStructure] = [
        mood,
        shape,
        color,
        taste,
        scent,
        media,
        music,
    ]
    for header, data in all_data:
        for value in data:
            url = f"http://192.168.1.64:5000/api/{header.name}/{value[0]}"
            body = dict(zip(header.attrs, value[1:]))
            logger.info("PUT %s (%s)", url, body)
            requests.put(url, json=body)

    c_header, results = connections
    for result in results:
        for qualia, table in zip(result[1:], c_header.attrs):
            url = f"http://192.168.1.64:5000/api/{table}s_{c_header.name}"
            body = {"mood": result[0], table: qualia}
            logger.info("POST %s (%s)", url, body)
            requests.post(url, json=body)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    populate()
