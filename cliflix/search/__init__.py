# sys.path.insert(0, str(Path.joinpath(Path(__file__).parent, "search")))
from cliflix.search.kickass_torrent import kickass_torrent
from cliflix.search.limetorrents import limetorrents
from cliflix.search.one337x import one337x
from cliflix.search.piratebay import piratebay
from cliflix.search.torrentproject import torrentproject
from cliflix.search.torrentscsv import torrentscsv
from cliflix.search.rarbg import rarbg
from cliflix.search.solidtorrents import solidtorrents

engines = {
    "kickass_torrent": kickass_torrent,
    "limetorrents": limetorrents,
    "one337x": one337x,
    "piratebay": piratebay,
    "rarbg": rarbg,

    "solidtorrents": solidtorrents,
    "torrentproject": torrentproject,
    "torrentscsv": torrentscsv
}
