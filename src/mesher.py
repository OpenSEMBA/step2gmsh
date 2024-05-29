import gmsh
from itertools import chain
from pathlib import Path

DEFAULT_MESHING_OPTIONS = {
    
    "Mesh.MshFileVersion": 2.2,   # Mandatory for MFEM compatibility
    "Mesh.MeshSizeFromCurvature": 50,
    "Mesh.ElementOrder": 3,
    "Mesh.ScalingFactor": 1e-3,
    "Mesh.SurfaceFaces": 1,
    "Mesh.MeshSizeMax": 50,

    "General.DrawBoundingBoxes": 1,
    "General.Axes": 1,

    "Geometry.SurfaceType": 2,    # Diplay surfaces as solids rather than dashed lines.
    # "Geometry.OCCBoundsUseStl": 1,
    # "Geometry.OCCSewFaces": 1,
    # "Geometry.Tolerance": 1e-3,
}

RUN_GUI=False

class ShapesClassification:
    def __init__(self, shapes):
        gmsh.model.occ.synchronize()

        self.allShapes = shapes

        self.pecs = self.get_surfaces_with_label(shapes, "Conductor_")
        self.dielectrics = self.get_surfaces_with_label(shapes, "Dielectric_")
        self.open = self.get_surfaces_with_label(shapes, "OpenRegion_")

        if len(self.open) > 1:
            raise ValueError("Only one open region is allowed.")

    @staticmethod
    def getNumberFromName(entity_name: str, label: str):
        ini = entity_name.rindex(label) + len(label)
        num = int(entity_name[ini:])
        return num

    @staticmethod
    def get_surfaces_with_label(entity_tags, label: str):
        surfaces = dict()
        for s in entity_tags:
            name = gmsh.model.get_entity_name(*s)
            if s[0] != 2 or label not in name:
                continue
            num = ShapesClassification.getNumberFromName(name, label)
            surfaces[num] = [s]

        return surfaces

    def isOpenOrSemiOpenProblem(self):
        return len(self.open) != 0

    def buildVacuumDomain(self):
        if self.isOpenOrSemiOpenProblem():
            dom = self.open[0]
        else:
            dom = self.pecs[0]

        surfsToRemove = []
        for num, surf in self.pecs.items():
            if num == 0 and self.isOpenOrSemiOpenProblem() == False:
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
                if num2 == 0 and not self.isOpenOrSemiOpenProblem():
                    continue
                pec_surfs.extend(pec_surf)
            self.dielectrics[num] = gmsh.model.occ.cut(diel, pec_surfs, removeTool=False)[0]

        gmsh.model.occ.synchronize()

    def ensureDielectricsDoNotOverlap(self):
        for n1, diel1 in self.dielectrics.items():
            others = list(
                chain(
                    *[x[1] for x in self.dielectrics.items() if x[0] != n1]
                )
            )

            if len(others) == 0:
                continue

            self.dielectrics[n1] = gmsh.model.occ.cut(
                self.dielectrics[n1], others, removeObject=True, removeTool=False)[0]

        gmsh.model.occ.synchronize()



def getPhysicalGrupWithName(name: str):
    pGs = gmsh.model.getPhysicalGroups()
    for pG in pGs:
        if gmsh.model.getPhysicalName(*pG) == name:
            return pG

def extractBoundaries(shapes: dict):
    shape_boundaries = dict()
    for num, surfs in shapes.items():
        bdrs = gmsh.model.getBoundary(surfs)
        shape_boundaries[num] = bdrs

    return shape_boundaries

def meshFromStep(
        inputFile: str,
        case_name: str,
        meshing_options=DEFAULT_MESHING_OPTIONS):
    gmsh.model.add(case_name)

    # Importing from FreeCAD generated steps.
    # STEP default units are mm.
    allShapes = ShapesClassification(
        gmsh.model.occ.importShapes(inputFile, highestDimOnly=False)
    )

    # --- Geometry manipulation ---
    # -- Domains
    allShapes.ensureDielectricsDoNotOverlap()
    allShapes.removeConductorsFromDielectrics()
    vacuumDomain = allShapes.buildVacuumDomain()

    # -- Boundaries
    pec_bdrs = extractBoundaries(allShapes.pecs)
    open_bdrs = extractBoundaries(allShapes.open)

    if len(open_bdrs) > 1:
        raise ValueError("Invalid number of open boundaries.")

    # In semi-open problems, conductors can intersect the open region.
    # Conductors have priority over the open boundary.    
    if len(open_bdrs) == 1:
        for num, pec_bdr in pec_bdrs.items():
            overlapping = gmsh.model.occ.intersect(
                open_bdrs[0], pec_bdr, removeObject=False, removeTool=False)[0]
            if len(overlapping) > 0:
                frag = gmsh.model.occ.fragment(
                    overlapping, vacuumDomain, removeObject=True, removeTool=False)[0]
                pec_bdrs[num] = [x for x in frag if x[0] == 1]
                vacuumDomain  = [x for x in frag if x[0] == 2]
        gmsh.model.occ.synchronize()

        toRemove = [x for bdrs in pec_bdrs.values() for x in bdrs]
        newOpenBdr = gmsh.model.occ.cut(open_bdrs[0], toRemove, removeObject=False, removeTool=False)[0]
        frag = gmsh.model.occ.fragment(
            newOpenBdr, vacuumDomain, removeObject=True, removeTool=False)[0]  
        open_bdrs[0]  = [x for x in frag if x[0] == 1]
        vacuumDomain  = [x for x in frag if x[0] == 2]
        gmsh.model.occ.synchronize()	    
    

    # --- Physical groups ---
    # Adds boundaries.
    for num, bdrs in pec_bdrs.items():
        name = "Conductor_" + str(num)
        tags = [x[1] for x in bdrs]
        gmsh.model.addPhysicalGroup(1, tags, name=name)

    for num, bdrs in open_bdrs.items():
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
    gmsh.model.remove_entities(entsNotInPG, recursive=False)
    
    # Meshing.
    for [opt, val] in meshing_options.items():
        gmsh.option.setNumber(opt, val)

    gmsh.model.mesh.generate(2)
    

def runFromInput(inputFile):
    case_name = Path(inputFile).stem

    gmsh.initialize()

    meshFromStep(inputFile, case_name, DEFAULT_MESHING_OPTIONS)   

    gmsh.write(case_name + '.msh')
    gmsh.write(case_name + '.vtk')
    gmsh.finalize()

def runCase(
        folder: str,
        case_name: str,
        meshing_options=DEFAULT_MESHING_OPTIONS):

    gmsh.initialize()

    inputFile = folder + case_name + '/' + case_name + ".step"
    meshFromStep(inputFile, case_name, meshing_options)
    
    gmsh.write(case_name + '.msh')
    if RUN_GUI: # for debugging only.
        gmsh.fltk.run()

    gmsh.finalize()
