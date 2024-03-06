import vtk
import numpy as np
import os

def load_vtk_vtp(fiber_vtk_name):
    basename, extension = os.path.splitext(fiber_vtk_name)
    if extension == ".vtk":
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(fiber_vtk_name)
        reader.Update()
        inpd = reader.GetOutput()
    elif extension == ".vtp":
        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName(fiber_vtk_name)
        reader.Update()
        inpd = reader.GetOutput()
    else:
        ValueError("File extension error.")

    return inpd


def write_vtk_vtp(lines_points, output_filename, additional_array):
    outpd = vtk.vtkPolyData()
    outpoints = vtk.vtkPoints()
    outlines = vtk.vtkCellArray()


    new_pointdata_array=vtk.vtkFloatArray()
    new_pointdata_array.SetName('color_index')

    outlines.InitTraversal()

    for lidx in range(0, len(lines_points)):
        cellptids = vtk.vtkIdList()

        for pidx in range(0, len(lines_points[lidx])):
            idx = outpoints.InsertNextPoint(lines_points[lidx][pidx][0],
                                            lines_points[lidx][pidx][1],
                                            lines_points[lidx][pidx][2])

            cellptids.InsertNextId(idx)

            new_pointdata_array.InsertNextTuple1(additional_array[lidx][pidx])

        outlines.InsertNextCell(cellptids)

    # put data into output polydata
    outpd.SetLines(outlines)
    outpd.SetPoints(outpoints)
    outpd.GetPointData().AddArray(new_pointdata_array)

    basename, extension = os.path.splitext(output_filename)
    if extension=='.vtk':
        writer = vtk.vtkDataSetWriter()
    elif extension=='.vtp':
        writer = vtk.vtkXMLPolyDataWriter()
    else:
        ValueError('Output file name error.')
    writer.SetFileName(output_filename)
    writer.SetInputData(outpd)
    writer.Write()

# ==================================================
# Time    :   2024/03/06 11:11:59
# Function:   set color map 
#             
# ==================================================

# load input vtk
inpd=load_vtk_vtp("C:\\Users\\ZhangWei\\Desktop\\our_atlas\\atlas_by_label\\CB\\CB.vtp")

# shape: lines' number * every line's points number * 3(single point:x,y,z)
lines=[]
# shape: line's number * every line's points number
lines_colors=[]
for line_index in range(inpd.GetNumberOfCells()):
    pts=inpd.GetCell(line_index).GetPoints()

    # get this line's all points
    line_points_np=np.array([np.array(pts.GetPoint(point_index)) for point_index in range(pts.GetNumberOfPoints())])
    # give every point a color
    line_color=[0.1 for i in range(int(pts.GetNumberOfPoints()/3))] + [0.5 for i in range(int(pts.GetNumberOfPoints()/3))] + [0.9 for i in range(pts.GetNumberOfPoints()-2*int(pts.GetNumberOfPoints()/3))]
    
    # save in our list
    lines.append(line_points_np)
    lines_colors.append(line_color)

# write in vtk or vtp
write_vtk_vtp(lines_points=lines,output_filename='./test.vtp',additional_array=lines_colors)

