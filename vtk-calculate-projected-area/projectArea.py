
import vtk
try:
    from vtk.util.numpy_support import vtk_to_numpy
    has_numpy = True
except ModuleNotFoundError:
    has_numpy = False


def load_stl(stl_file:str):
    """ Load STL file 
    TODO: maybe remove this, only called once!
    """
    reader = vtk.vtkSTLReader()
    reader.SetFileName(stl_file)
    reader.Update()
    return reader.GetOutput()


def project(stl_file:str,direction:str='x',scale:int=2,verbose:bool=False):
    """ Calculate the projected area of a STL geometry

    Uses the pixels in the rendered image to estimate the projected area.
    Based on code by Paul McIntosh: 
      github.com/internetscooter/Vespa-Labs/blob/master/VespaCFD/CalculateFrontalArea/CalculateFrontalArea.cxx
    
    For simplicity, only considers cartesian directions (x, y and z) for the 
    moment, but it can be easily be adapted to accept any vector as the
    projection direction.

    There is no unit, you should consider the square value of the input
    stl unit.


    Arguments:

        stl_file: path to the stl file
        direction: string with the direction of the projection. Optional,
           the default is `x`.
        scale: factor for scaling the produced image. A higher value leads to
           a more precise estimation. Optional, the default is 2
           (image will be 600 x 600).
        verbose: print details of calculation (pixel count, resolution).
           Optional, default is False.

    Returns:

        area: estimate projected area in (stl dimensional unit)^2
        resolution: pixel resoution in (stl dimensional unit)^2
    
    """

    directions = {
        'x':dict(orientation=(1,0,0),view_up=(0,0,1)),
        'y':dict(orientation=(0,1,0),view_up=(0,0,1)),
        'z':dict(orientation=(0,0,1),view_up=(0,1,0)),
    }

    poly_data = load_stl(stl_file)

    mapper_data = vtk.vtkPolyDataMapper()
    mapper_data.SetInputData(poly_data)
    actor_data = vtk.vtkActor()
    actor_data.SetMapper(mapper_data)
    actor_data.GetProperty().SetColor([0,0,0])
    actor_data.GetProperty().SetRepresentationToSurface()
    actor_data.GetProperty().SetEdgeColor(0,0,0)
    
    renderer = vtk.vtkRenderer()
    renderer.SetBackground([1,1,1])
    renderer.AddActor(actor_data)
    renderer.ResetCamera()
    renderer.GetActiveCamera().SetParallelProjection(1)

    camera = renderer.GetActiveCamera()
    camera.ParallelProjectionOn()
    center = poly_data.GetCenter()
    camera.SetPosition(
        *[c - o for c,o in zip(center,directions[direction]['orientation'])]
        )
    camera.SetFocalPoint(*center)
    camera.SetViewUp(*directions[direction]['view_up'])
    renderer.ResetCamera()

    render_window = vtk.vtkRenderWindow()
    render_window.SetOffScreenRendering(1)
    render_window.AddRenderer(renderer)
    render_window.Render()
    render_window.SetAlphaBitPlanes(1) # enable usage of alpha channel

    # Get a print of the window
    window_to_image = vtk.vtkWindowToImageFilter()
    window_to_image.SetInput(render_window)
    window_to_image.SetScale(scale) # image quality
    window_to_image.SetInputBufferTypeToRGBA()
    window_to_image.Update()

    imageData = vtk.vtkImageData()
    imageData = window_to_image.GetOutput()
    
    dimensions = imageData.GetDimensions()
    resolution = camera.GetParallelScale()*camera.GetParallelScale()*4 / (dimensions[0]*dimensions[0])
    if not has_numpy:
        count = 0
        for y in range(dimensions[1]):
            for x in range(dimensions[0]):
                pixel = imageData.GetScalarComponentAsFloat(x,y,0,0)
                if (pixel == 255): pass
                else: count += 1
    else:
        array = vtk_to_numpy(imageData.GetPointData().GetScalars())
        mask = array[:,0] != 255
        count = mask.sum()

    area = count * resolution

    if verbose:
        print(f'- file: {stl_file}')
        print(f'- image dimension: {dimensions}')
        print(f'- total pixels: {dimensions[0]*dimensions[1]*dimensions[2]:,}',)
        print(f'- projected pixels: {count:,}')
        print(f'- resolution: {resolution:.5e}')
        print(f'- area: {area:.5e}')
        print('')

    return area, resolution


if __name__ == '__main__':
    # to implement
    pass