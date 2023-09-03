"""

Generate sample STL of canonical shapes:

- cube: side 1.0 x 1.0 x 1.0
- sphere: radius = 1.0
- cone: radius = 1.0, height = 2.0
- disk: inner radius = 0.5, outer radius = 1.0
- torus: torus radius = 1.0, section radius = 0.5

"""

import pathlib
import vtk

output_folder = pathlib.Path('./geometry')
output_folder.mkdir(parents=True,exist_ok=True)

writer = vtk.vtkSTLWriter()

cube = vtk.vtkCubeSource()
writer.SetFileName( str( output_folder / 'cube.stl' ) )
writer.SetInputConnection(cube.GetOutputPort())
writer.Write()

sphere = vtk.vtkSphereSource()
sphere.SetRadius(1.0)
sphere.SetPhiResolution(100)
sphere.SetThetaResolution(100)
writer.SetFileName( str( output_folder / 'sphere.stl') )
writer.SetInputConnection(sphere.GetOutputPort())
writer.Write()

cone = vtk.vtkConeSource()
cone.SetResolution(200)
cone.SetRadius(1.0)
cone.SetHeight(2.0)
writer.SetFileName( str( output_folder / 'cone.stl' ) )
writer.SetInputConnection(cone.GetOutputPort())
writer.Write()

disk = vtk.vtkDiskSource()
disk.SetCircumferentialResolution(200)
disk.SetRadialResolution(5)
disk.SetInnerRadius(0.5)
disk.SetOuterRadius(1.0)
writer.SetFileName( str( output_folder / 'disk.stl' ) )
writer.SetInputConnection(disk.GetOutputPort())
writer.Write()

torus = vtk.vtkParametricFunctionSource()
torus.SetParametricFunction(vtk.vtkParametricTorus())
torus.SetUResolution(200)
torus.SetVResolution(200)
torus.SetWResolution(200)
torus.Update()
writer.SetFileName( str( output_folder / 'torus.stl' ) )
writer.SetInputConnection(torus.GetOutputPort())
writer.Write()
