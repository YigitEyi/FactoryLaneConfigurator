from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Tuple
import math

class Coordinates(BaseModel):
    x: float = Field(..., description="x coordinate")
    y: float = Field(..., description="y coordinate")
    
    def __str__(self):
        """String representation: (x, y)"""
        return f"({self.x:.2f}, {self.y:.2f})"
    def distance_to(self, other: 'Coordinates') -> float:
        """Calculate Euclidean distance to another Coordinates instance."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def asTuple(self) -> Tuple[float, float]:
        """Return coordinates as a tuple (x, y)."""
        return (self.x, self.y)
    
class Station(BaseModel):
    id: str = Field(..., description="Unique identifier for the station")
    coordinate: Coordinates
    name: str = Field(..., description="Name of the station")
    
    @field_validator('id')
    def validate_id(cls,v):
        if not v.strip():
            raise ValueError("Station ID cannot be empty")
        return v
    
    @property
    def location(self) -> Tuple[float, float]:
        """Return the station's coordinates as a tuple (x, y)."""
        return self.coordinate.asTuple()
    
    def __str__(self):
        """String representation: Station Name (ID) at (x, y)"""
        return f"{self.name} at {self.coordinate}"

class Junction(BaseModel):
    id : str = Field(..., description="Unique identifier for the junction")
    coordinate: Coordinates
    junction_type: str = Field(..., description="Type of the junction")
    junc_name: str = Field(..., description="Name of the junction")
    
    @field_validator('id')
    def validate_id(cls,v):
        if not v.strip():
            raise ValueError("Junction ID cannot be empty")
        return v
    @property
    def location(self) -> Tuple[float, float]:
        """Return the junction's coordinates as a tuple (x, y)."""
        return self.coordinate.asTuple()
    def __str__(self):
        """String representation: Junction Type (ID) at (x, y)"""
        return f"{self.junc_name} Junction at {self.coordinate}"
        
class FactoryLayout(BaseModel):
    stations: List[Station] = Field(..., description="List of stations in the factory layout")
    junctions: List[Junction] = Field(..., description="List of junctions in the factory layout")
    connections: Dict[str, List[str]] = Field(..., description="Mapping of station/junction IDs to connected IDs")

    def get_station_by_id(self, station_id: str) -> Optional[Station]:
        """Retrieve a station by its ID."""
        for station in self.stations:
            if station.id == station_id:
                return station
        return None

    def get_junction_by_id(self, junction_id: str) -> Optional[Junction]:
        """Retrieve a junction by its ID."""
        for junction in self.junctions:
            if junction.id == junction_id:
                return junction
        return None

    def get_all_nodes(self) -> List[Tuple[str, Coordinates]]:
        """Get a list of all stations and junctions with their coordinates."""
        nodes = []
        for station in self.stations:
            nodes.append((station.name, station.coordinate))
        for junction in self.junctions:
            nodes.append((junction.junc_name, junction.coordinate))
        return nodes

    def get_all_coordinates(self) -> List[Coordinates]:
        """Get a list of all coordinates of stations and junctions."""
        coords = [station.coordinate for station in self.stations]
        coords.extend(junction.coordinate for junction in self.junctions)
            return coords