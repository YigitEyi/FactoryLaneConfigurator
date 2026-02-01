import ezdxf
from typing import List, Optional
from pathlib import Path
import logging

from src.core.models import Station, Junction, Coordinate, FactoryLayout
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DXFParser:
    STATION_LAYER = "AGV_NOKTALARı"
    ROUTE_LAYER = "UH6"
    def __init__(self, file_path: str):
        self.doc = ezdxf.readfile(file_path)
        self.modelspace = self.doc.modelspace()
        
    def extract_stations(self) -> List[Station]:
        stations = []
        for entity in self.modelspace.query('MTEXT[layer=="{}"]'.format(self.STATION_LAYER)):
            text = entity.plain_text().strip()
            if text.isdigit():
                station_id = text
                coordinate = Coordinate(x=entity.dxf.insert.x, y=entity.dxf.insert.y)
            station = Station(id=station_id, name=f"Station {station_id}", coordinate=coordinate)
            stations.append(station)
            logger.info(f"Extracted {station}")
        return stations
    