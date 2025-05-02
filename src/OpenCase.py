from typing import Any, Tuple, List, Dict
import gmsh
from test import utils
class BoundingBox():
    edges: Dict[str, float]
    def __init__(self, listOfCoordinates:Tuple[int, int, int, int, int, int]):
        self.edges = {
                'xmin': listOfCoordinates[0],
                'ymin': listOfCoordinates[1],
                'zmin': listOfCoordinates[2],
                'xmax': listOfCoordinates[3],
                'ymax': listOfCoordinates[4],
                'zmax': listOfCoordinates[5],
            }
        
    def getCenter(self) -> Tuple[float,float,float]:
        return (
            (self.edges['xmax'] + self.edges['xmin']) / 2,
            (self.edges['ymax'] + self.edges['ymin']) / 2,
            (self.edges['zmax'] + self.edges['zmin']) / 2
        )
    def getDiagonal(self) -> float:
        dx = self.edges['xmax'] - self.edges['xmin']
        dy = self.edges['ymax'] - self.edges['ymin']
        dz = self.edges['zmax'] - self.edges['zmin']
        return (dx**2 + dy**2 + dz**2) ** 0.5

        
class OpenMultiwire():
    def __init__(self, listCoductors: Any, listDielectrics:Any) -> None:
        gmsh.model.occ.synchronize()
        self.listCoductors = listCoductors
        self.listDielectrics = listDielectrics

    @staticmethod
    def _getBoundingBox(element:Tuple[int,int]) -> BoundingBox:
        boundingBox:BoundingBox = BoundingBox(gmsh.model.occ.get_bounding_box(*element))
        return boundingBox

    @staticmethod
    def getBoundingBoxFromGroup(elements:List[Tuple[int,int]]) -> BoundingBox:
        boundingBoxs:List[BoundingBox] = []
        for element in elements:
            boundingBoxs.append(OpenMultiwire._getBoundingBox(element))
        
        if len(boundingBoxs) != 0:
            edges: Dict[str, List[float]] = {
                'xmin': [],
                'ymin': [],
                'zmin': [],
                'xmax': [],
                'ymax': [],
                'zmax': [],
            }
            for boundingBox in boundingBoxs:
                for key in edges.keys():
                    edges[key].append(boundingBox.edges[key])
            
            return BoundingBox(
                (
                    utils.getMinFromList(edges['xmin']),
                    utils.getMinFromList(edges['ymin']),
                    utils.getMinFromList(edges['zmin']),
                    utils.getMaxFromList(edges['xmax']),
                    utils.getMaxFromList(edges['ymax']),
                    utils.getMaxFromList(edges['zmax'])
                )
            )
        else:
            return BoundingBox((0,0,0,0,0,0))
        

        