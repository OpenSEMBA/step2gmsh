import gmsh
import sys
from collections import defaultdict

DEFAULT_MESHING_OPTIONS = {
    "Mesh.MshFileVersion": 2.2,
    "Mesh.MeshSizeFromCurvature": 40,
    "Mesh.ElementOrder": 3,
    "Mesh.ScalingFactor": 1e-3,
    "Mesh.SurfaceFaces": 1,
    # "Mesh.MeshSizeMax": 10,
    "General.DrawBoundingBoxes": 1
}

RUN_GUI=False

class ShapesClassification:
    def __init__(self, shapes):
        gmsh.model.occ.synchronize()

        self.allShapes = shapes

        self.pecs = self.get_surfaces(shapes, "Conductor_")
        self.dielectrics = self.get_surfaces(shapes, "Dielectric_")
        self.open = self.get_surfaces(shapes, "OpenRegion_")

        if len(self.open) > 1:
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
            surfaces[num] = [s]

        return surfaces

    def isOpenProblem(self):
        return len(self.open) != 0

    def buildVacuumDomain(self):
        if self.isOpenProblem():
            dom = self.open[0]
        else:
            dom = self.pecs[0]

        surfsToRemove = []
        for num, surf in self.pecs.items():
            if num == 0 and self.isOpenProblem() == False:
                continue
            surfsToRemove.extend(surf)

        for _, surf in self.dielectrics.items():
            surfsToRemove.extend(surf)

        dom = gmsh.model.occ.cut(
            dom, surfsToRemove, removeObject=False, removeTool=False)[0]
        gmsh.model.occ.synchronize()

        return dom
    
    def removeConductorsFromDielectrics(self):
        for num, diel in self.dielectrics.items():
            pec_surfs = []
            for num2, pec_surf in self.pecs.items():
                if num2 == 0 and not self.isOpenProblem():
                    continue
                pec_surfs.extend(pec_surf)
            self.dielectrics[num] = gmsh.model.occ.cut(diel, pec_surfs, removeTool=False)[0]

        gmsh.model.occ.synchronize()


def getPhysicalGrupWithName(name: str):
    pGs = gmsh.model.getPhysicalGroups()
    for pG in pGs:
        if gmsh.model.getPhysicalName(*pG) == name:
            return pG

def extractBoundaries(shapes: dict):
    shape_boundaries = dict()
    for num, bdrs in shapes.items():
        shape_boundaries[num] = gmsh.model.getBoundary(bdrs)

    return shape_boundaries

def meshFromStep(
        folder: str,
        case_name: str,
        meshing_options=DEFAULT_MESHING_OPTIONS):
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
    # -- Domains
    allShapes.removeConductorsFromDielectrics()
    vacuumDomain = allShapes.buildVacuumDomain()

    # -- Boundaries
    pec_bdrs = extractBoundaries(allShapes.pecs)
    gmsh.model.occ.synchronize()

    # --- Physical groups ---
    # Adds boundaries.
    for num, bdrs in pec_bdrs.items():
        name = "Conductor_" + str(num)
        tags = [x[1] for x in bdrs]
        gmsh.model.addPhysicalGroup(1, tags, name=name)

    for num, bdrs in extractBoundaries(allShapes.open).items():
        name = "OpenRegion_" + str(num)
        tags = [x[1] for x in bdrs if x[1] > 0]
        gmsh.model.addPhysicalGroup(1, tags, name=name)

    # Domains.
    gmsh.model.addPhysicalGroup(2, [x[1] for x  in vacuumDomain], name='Vacuum')

    for num, surfs in allShapes.dielectrics.items():
        name = "Dielectric_" + str(num)
        tags = [x[1] for x in surfs]
        gmsh.model.addPhysicalGroup(2, tags, name=name)

    # Removes entities which are not at least in one physical group.
    allEnts = gmsh.model.get_entities()

    entsInPG = []
    for pG in gmsh.model.get_physical_groups():
        ents = gmsh.model.getEntitiesForPhysicalGroup(pG[0], pG[1])
        for ent in ents:
            entsInPG.append((pG[0], ent))

    entsNotInPG = [x for x in allEnts if x not in entsInPG]
    gmsh.model.remove_entities(entsNotInPG)

    # Meshing.
    for [opt, val] in meshing_options.items():
        gmsh.option.setNumber(opt, val)

    gmsh.model.mesh.generate(2)
    

def runStepToGmsh(
        folder: str,
        case_name: str,
        meshing_options=DEFAULT_MESHING_OPTIONS):

    gmsh.initialize()

    meshFromStep(folder, case_name, meshing_options)
    
    gmsh.write(case_name + '.msh')
    if RUN_GUI: # for debugging only.
        gmsh.fltk.run()

    gmsh.finalize()
