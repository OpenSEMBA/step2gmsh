from typing import Any, Tuple, List, Dict
import gmsh

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
        
class OpenMultiwire():
    def __init__(self, listCoductors: Any, listDielectrics:Any) -> None:
        gmsh.model.occ.synchronize()
        self.listCoductors = listCoductors
        self.listDielectrics = listDielectrics

    @staticmethod
    def _getBoundingBox(element:Tuple[int,int]) -> BoundingBox:
        boundingBox:BoundingBox = BoundingBox(gmsh.model.occ.get_bounding_box(*element))
        return boundingBox

    def getBoundingBoxFromGroup(self, elements:List[Tuple[int,int]]) -> BoundingBox:
        boundingBoxs:List[BoundingBox] = []
        for element in elements:
            boundingBoxs.append(self._getBoundingBox(element))
        
        if len(boundingBoxs) != 0:
            edges: Dict[str, Tuple[float]] = {
                'xmin': (),
                'ymin': (),
                'zmin': (),
                'xmax': (),
                'ymax': (),
                'zmax': (),
            }
            for boundingBox in boundingBoxs:
                for key in edges.items():
                    edges[key] = edges[key].append(boundingBox.edges[key])

        else:
            return BoundingBox((0,0,0,0,0,0))
        

        