import rhinoscriptsyntax as rs


def main():
    #objectIn = rs.GetObject("select a point",1)
    #object = rs.coerce3dpoint(objectIn)
    #print "point at:"+ str(object.X) + "," + str(object.Y) + "," + str(object.Z)
    
    curveIn = rs.GetObject("select a curve",4)
    curveObject = rs.coercecurve(curveIn)
    #print "curve with " + str(curve.PointCount-1) + " points"
    
    boundingBox = curveObject.GetBoundingBox(True)
    center = boundingBox.Center
    print "center of curve at " +str(center.X) +str(center.Y)+str(center.Z) 
    #rs.AddPoint(center)
    
    newCurves = rs.ExplodeCurves(curveIn)
    
    for curve in newCurves:
        pts = []
        pts.append(rs.CurveStartPoint(curve))
        pts.append(rs.CurveEndPoint(curve))
        pts.append(center)
        pts.append(rs.CurveStartPoint(curve))
        
        triangleCurve = rs.AddCurve(pts,1)
        roundCurve = rs.AddCurve(pts,3)
        
        surface = rs.AddPlanarSrf(triangleCurve)
        newSurfs = trimSurfaceWithCurve(surface,roundCurve)
        rs.DeleteObject(surface)

def trimSurfaceWithCurve(surface, curve):
    centroid = rs.SurfaceAreaCentroid(surface)
    domain_u = rs.SurfaceDomain(surface, 0)
    domain_v = rs.SurfaceDomain(surface, 1)
    normal = rs.SurfaceNormal(surface, [domain_u[0],domain_v[0]])
    tempLine = rs.AddLine(centroid[0],rs.PointAdd(normal,centroid[0]))
    
    extrudeSrf = rs.ExtrudeCurve(curve,tempLine)
    rs.DeleteObject(tempLine)
    
    newSrfs = rs.SplitBrep(surface,extrudeSrf)
    rs.DeleteObject(extrudeSrf)
    maxArea = 0
    minArea = 9999999999
    for srf in newSrfs:
        area = rs.Area(srf)
        if area>maxArea:
            deleteSrf = srf
            maxArea = area
        if area < minArea:
            returnSrf = srf
            minArea = area
    rs.DeleteObject(deleteSrf)
    return returnSrf
    
    





if __name__=="__main__":
    main()
