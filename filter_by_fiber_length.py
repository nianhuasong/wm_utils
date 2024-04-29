import argparse
import os
import vtk
import numpy as np
import math

def compute_length(point1, point2):
    length = math.sqrt(
        abs(point1[0] - point2[0]) ** 2 + abs(point1[1] - point2[1]) ** 2 + abs(point1[2] - point2[2]) ** 2)
    return length


def filter_fiber(fiber_vtk_name, output_name):
    # read vtk/vtp
    basename, extension = os.path.splitext(fiber_vtk_name)
    if extension == '.vtk':
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(fiber_vtk_name)
        reader.Update()
        inpd = reader.GetOutput()
    else:
        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName(fiber_vtk_name)
        reader.Update()
        inpd = reader.GetOutput()

    # get point data 
    inpointdata = inpd.GetPointData()
    # get array and their name in point data
    f2_array = inpointdata.GetArray(0)
    f2_array_name = f2_array.GetName()
    estimated_array = inpointdata.GetArray(1)
    estimated_array_name = estimated_array.GetName()
    f1_array = inpointdata.GetArray(2)
    f1_array_name = f1_array.GetName()

    # create new array, new points, new lines
    f1_new_array = vtk.vtkFloatArray()
    f1_new_array.SetName(f1_array_name)
    f2_new_array = vtk.vtkFloatArray()
    f2_new_array.SetName(f2_array_name)
    estimated_new_array = vtk.vtkFloatArray()
    estimated_new_array.SetName(estimated_array_name)
    outpoints = vtk.vtkPoints()
    outlines = vtk.vtkCellArray()
    outlines.InitTraversal()

    # traverse every point in every line
    inpd.GetLines().InitTraversal()
    for lidx in range(0, inpd.GetNumberOfLines()):
        ptids = vtk.vtkIdList()
        inpd.GetLines().GetNextCell(ptids)
        num_points = ptids.GetNumberOfIds()
        head_point = inpd.GetPoints().GetPoint(ptids.GetId(0))
        end_point = inpd.GetPoints().GetPoint(ptids.GetId(num_points - 1))
        # compute length
        length = compute_length(head_point, end_point)
        # >= threshould value
        if length >= int(args.filter_length):
            
            out_ptids = vtk.vtkIdList()
            for ptid in range(0, num_points):
                # add new points 
                point = inpd.GetPoints().GetPoint(ptids.GetId(ptid))
                idx = outpoints.InsertNextPoint(point)
                out_ptids.InsertNextId(idx)

                # get old array
                f1 = f1_array.GetTuple(ptids.GetId(ptid))[0]
                f2 = f2_array.GetTuple(ptids.GetId(ptid))[0]
                estimated = estimated_array.GetTuple(ptids.GetId(ptid))[0]

                # add new array
                f1_new_array.InsertNextTuple1(f1)
                f2_new_array.InsertNextTuple1(f2)
                estimated_new_array.InsertNextTuple1(estimated)

            # add new lines
            outlines.InsertNextCell(out_ptids)

    # create new vtk
    outpd = vtk.vtkPolyData()
    outpd.SetLines(outlines)
    outpd.SetPoints(outpoints)
    outpd.GetPointData().AddArray(f2_new_array)
    outpd.GetPointData().AddArray(estimated_new_array)
    outpd.GetPointData().AddArray(f1_new_array)

    writer = vtk.vtkDataSetWriter()
    writer.SetFileName(output_name)
    writer.SetInputData(outpd)
    writer.Write()

    return 0


# ------------------
# Parse arguments
# ------------------
parser = argparse.ArgumentParser(description="Filter the fiber tract of vtk file by length.",
                                 epilog='Written by Wei Zhang')
parser.add_argument('inputVTK', help='input vtk')
parser.add_argument('outputVTK', help='output vtk')
parser.add_argument('filter_length', help='min length to filter fibers')
args = parser.parse_args()

status = filter_fiber(args.inputVTK, args.outputVTK)

print('<length_filter>', args.outputVTK)