/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright (C) 2018 Tomislav Maric, TU Darmstadt 
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Application

    foamWritePointsToVtk

Description

    Minimal example showing how to write a set of points into VTK. 

\*---------------------------------------------------------------------------*/

// VTK output dependencies.
#include "foamVtkLegacyAsciiFormatter.H"
#include "foamVtkOutput.H"
#include "pointList.H"
#include "point.H"
#include "List.H"
#include "pointList.H"
#include <fstream>

// Testing dependencies

// Only use this in application cod. 
using namespace Foam;
using namespace Foam::vtk;

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

int main(int argc, char *argv[])
{
    // A set of test points.  
    pointList testPoints = {point(0,0,0), point(1,0,0), 
                            point(1,1,0), point(0,1,0), 
                            point(0.5,0.5,1)}; 

    // Open file for output in overwrite mode.
    std::ofstream vtkFile("square.vtk"); 

    // Initialize the VTK formatter, legacy in this case.
    legacyAsciiFormatter legacyFormat(vtkFile, 15); 

    // Write the file header based on the chosen format (legacy VTK).
    legacy::fileHeader(legacyFormat, "testPoints", vtk::fileTag::POLY_DATA);

    // Write the points beginning line for legacy VTK.  
    legacy::beginPoints(vtkFile, testPoints.size());

    // Write the list of points using the legacy formatter.
    writeList(legacyFormat, testPoints); 

    return 0;
}


// ************************************************************************* //
