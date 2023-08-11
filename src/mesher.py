import gmsh
import sys
from collections import defaultdict

DEFAULT_MESHING_OPTIONS = {
    "Mesh.MeshSizeFromCurvature": 25,
    "Mesh.ElementOrder": 3,
    "Mesh.ScalingFactor": 1e-3,
    "Mesh.SurfaceFaces": 1,
    "Mesh.MeshSizeMax": 1,
    "General.DrawBoundingBoxes": 1,
}


class ShapesClassification:
    def __init__(self, shapes):
        gmsh.model.occ.synchronize()

        self.allShapes = shapes

        self.pecs = self.get_surfaces(shapes, "Conductor_")
        self.dielectrics = self.get_surfaces(shapes, "Dielectric_")
        self.open = self.get_surfaces(shapes, "OpenRegion_")

        if len(self.open > 1):
            raise ValueError("Only one open region is allowed.")

    @staticmethod
    def getNumberFromEntityName(entity_name: str, label: str):
        ini = entity_name.rindex(label) + len(label)
        num = int(entity_name[ini:])
        return num

    @staticmethod
    def get_surfaces(shapes, label: str):
        surfaces = dict()
        for s in shapes:
            entity_name = gmsh.model.get_entity_name(*s)
            if s[0] != 2 or label not in entity_name:
                continue
            num = ShapesClassification.getNumberFromEntityName(
                entity_name, label)
            surfaces[num] = s

        return surfaces


def extractBoundaries(shapes: dict):
    shape_boundaries = dict()
    for num, surf in shapes.items():
        shape_boundaries[num] = gmsh.model.getBoundary([surf])
    return shape_boundaries


def meshFromStep(
        folder: str,
        case_name: str,
        meshing_options=DEFAULT_MESHING_OPTIONS,
        runGUI: bool = False):

    gmsh.initialize()
    gmsh.model.add(case_name)

    # Importing from FreeCAD generated steps.
    # STEP default units are mm.
    allShapes = ShapesClassification(
        gmsh.model.occ.importShapes(
            folder + case_name + '/' + case_name + '.step',
            highestDimOnly=False
        )
    )

    # --- Geometry manipulation ---
    # Creates global domain.
    if len(allShapes.open) != 0:
        isOpenProblem = True
        globalDomain = allShapes.open[0]
    else:
        isOpenProblem = False
        globalDomain = allShapes.pecs[0]

    for num, surf in allShapes.pecs.items():
        if num == 0 and isOpenProblem == False:
            continue
        for _, dielectric_surf in allShapes.dielectrics.items():
            gmsh.model.occ.cut([dielectric_surf], [surf], removeTool=False)
        gmsh.model.occ.cut([globalDomain], [surf], removeTool=False)

    for _, surf in allShapes.dielectrics.items():
        gmsh.model.occ.cut([globalDomain], [surf], removeTool=False)

    gmsh.model.occ.synchronize()

    pec_bdrs = extractBoundaries(allShapes.pecs)
    open_bdrs = extractBoundaries(allShapes.open)

    for num, surf in allShapes.pecs.items():
        if num != 0:
            gmsh.model.occ.remove([surf])
        elif num == 0 and isOpenProblem:
            gmsh.model.occ.remove([surf])

    gmsh.model.occ.synchronize()

    # --- Physical groups ---
    # Adds boundaries.
    for num, bdrs in pec_bdrs.items():
        name = "Conductor_" + str(num)
        for bdr in bdrs:
            if bdr[1] > 0:
                gmsh.model.addPhysicalGroup(1, [bdr[1]], name=name)
    
    if len(open_bdrs) > 0:
        gmsh.model.addPhysicalGroup(1, open_bdrs)

    # Domains.
    gmsh.model.addPhysicalGroup(2, [globalDomain[1]], name='Vacuum')

    for num, surf in allShapes.dielectrics.items():
        name = "Dielectric_" + str(num)
        gmsh.model.addPhysicalGroup(2, [surf[1]], name=name)

    # Meshing.
    for [opt, val] in meshing_options.items():
        gmsh.option.setNumber(opt, val)

    gmsh.model.mesh.generate(2)
    gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)

    # Exporting
    gmsh.write(case_name + '.msh')

    if runGUI:
        gmsh.fltk.run()

    gmsh.finalize()
