# trace generated using paraview version 5.11.2
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import os

# ファイルと同じ階層のパスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# create a new 'OpenFOAMReader'
postfoam = OpenFOAMReader(registrationName='post.foam', FileName=os.path.join(current_dir, 'post.foam'))
postfoam.MeshRegions = ['internalMesh']
postfoam.CellArrays = ['U', 'epsilon', 'k', 'nut', 'p', 'yPlus']

# get animation scene
animationScene1 = GetAnimationScene()

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
postfoamDisplay = Show(postfoam, renderView1, 'UnstructuredGridRepresentation')

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')

# trace defaults for the display properties.
postfoamDisplay.Representation = 'Surface'
postfoamDisplay.ColorArrayName = ['POINTS', 'p']
postfoamDisplay.LookupTable = pLUT
postfoamDisplay.SelectTCoordArray = 'None'
postfoamDisplay.SelectNormalArray = 'None'
postfoamDisplay.SelectTangentArray = 'None'
postfoamDisplay.OSPRayScaleArray = 'p'
postfoamDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
postfoamDisplay.SelectOrientationVectors = 'U'
postfoamDisplay.SelectScaleArray = 'p'
postfoamDisplay.GlyphType = 'Arrow'
postfoamDisplay.GlyphTableIndexArray = 'p'
postfoamDisplay.GaussianRadius = 0.05
postfoamDisplay.SetScaleArray = ['POINTS', 'p']
postfoamDisplay.ScaleTransferFunction = 'PiecewiseFunction'
postfoamDisplay.OpacityArray = ['POINTS', 'p']
postfoamDisplay.OpacityTransferFunction = 'PiecewiseFunction'
postfoamDisplay.DataAxesGrid = 'GridAxesRepresentation'
postfoamDisplay.PolarAxes = 'PolarAxesRepresentation'
postfoamDisplay.ScalarOpacityFunction = pPWF
postfoamDisplay.ScalarOpacityUnitDistance = 0.18971608552918393
postfoamDisplay.OpacityArrayName = ['POINTS', 'p']
postfoamDisplay.SelectInputVectors = ['POINTS', 'U']
postfoamDisplay.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
postfoamDisplay.ScaleTransferFunction.Points = [-0.8240132331848145, 0.0, 0.5, 0.0, 0.5972362756729126, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
postfoamDisplay.OpacityTransferFunction.Points = [-0.8240132331848145, 0.0, 0.5, 0.0, 0.5972362756729126, 1.0, 0.5, 0.0]

# reset view to fit data
renderView1.ResetCamera(False)

# show color bar/color legend
postfoamDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get 2D transfer function for 'p'
pTF2D = GetTransferFunction2D('p')

animationScene1.GoToLast()

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=postfoam)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.0, 0.5, 0.5]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [0.0, 0.5, 0.5]

# Properties modified on slice1.SliceType
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# show data in view
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['POINTS', 'p']
slice1Display.LookupTable = pLUT
slice1Display.SelectTCoordArray = 'None'
slice1Display.SelectNormalArray = 'None'
slice1Display.SelectTangentArray = 'None'
slice1Display.OSPRayScaleArray = 'p'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'U'
slice1Display.SelectScaleArray = 'p'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'p'
slice1Display.GaussianRadius = 0.05
slice1Display.SetScaleArray = ['POINTS', 'p']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = ['POINTS', 'p']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'
slice1Display.SelectInputVectors = ['POINTS', 'U']
slice1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
slice1Display.ScaleTransferFunction.Points = [-0.61735600233078, 0.0, 0.5, 0.0, 0.6240969896316528, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
slice1Display.OpacityTransferFunction.Points = [-0.61735600233078, 0.0, 0.5, 0.0, 0.6240969896316528, 1.0, 0.5, 0.0]

# hide data in view
Hide(postfoam, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, True)

# get layout
layout1 = GetLayout()

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)

# layout/tab size in pixels
layout1.SetSize(1272, 1112)

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, 0.5, 21.48528044351868]
renderView1.CameraFocalPoint = [0.0, 0.5, 0.5]
renderView1.CameraParallelScale = 5.431390245600108
renderView1.CameraParallelProjection = 1

# save screenshot
SaveScreenshot(os.path.join(current_dir, "..", 'p_planeZ.png'), renderView1, ImageResolution=[1272, 1112])

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'U', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('U')

# get opacity transfer function/opacity map for 'U'
uPWF = GetOpacityTransferFunction('U')

# get 2D transfer function for 'U'
uTF2D = GetTransferFunction2D('U')

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, True)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)

# layout/tab size in pixels
layout1.SetSize(1272, 1112)

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, 0.5, 21.48528044351868]
renderView1.CameraFocalPoint = [0.0, 0.5, 0.5]
renderView1.CameraParallelScale = 5.431390245600108
renderView1.CameraParallelProjection = 1

# save screenshot
SaveScreenshot(os.path.join(current_dir, "..", 'U_planeZ.png'), renderView1, ImageResolution=[1272, 1112])

renderView1.ResetActiveCameraToPositiveY()

# reset view to fit data
renderView1.ResetCamera(False)

# Properties modified on slice1.SliceType
slice1.SliceType.Normal = [0.0, 1.0, 0.0]

# update the view to ensure updated data information
renderView1.Update()

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, True)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)

# layout/tab size in pixels
layout1.SetSize(1272, 1112)

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, -24.68233653222242, 0.5]
renderView1.CameraFocalPoint = [0.0, 0.5, 0.5]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 6.51766829472013
renderView1.CameraParallelProjection = 1

# save screenshot
SaveScreenshot(os.path.join(current_dir, "..", 'U_planeY.png'), renderView1, ImageResolution=[1272, 1112])

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'p'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(uLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, True)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)

# layout/tab size in pixels
layout1.SetSize(1272, 1112)

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, -24.68233653222242, 0.5]
renderView1.CameraFocalPoint = [0.0, 0.5, 0.5]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 6.51766829472013
renderView1.CameraParallelProjection = 1

# save screenshot
SaveScreenshot(os.path.join(current_dir, "..", 'p_planeY.png'), renderView1, ImageResolution=[1272, 1112])

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1272, 1112)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, -24.68233653222242, 0.5]
renderView1.CameraFocalPoint = [0.0, 0.5, 0.5]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 6.51766829472013
renderView1.CameraParallelProjection = 1

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).