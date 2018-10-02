import c4d
#Welcome to the world of Python

prevMat = None
prevFrame = None

def GetPointsOfFace(myObj, myDir):
    selectedPoints = []
    polyCnt = myObj.GetPolygonCount()
    for x in range(0, polyCnt):
        polygon = myObj.GetPolygon(x)
        p0 = myObj.GetPoint(polygon.a)
        p1 = myObj.GetPoint(polygon.b)
        p2 = myObj.GetPoint(polygon.c)
        thisNormal = (p1 - p0).Cross(p2 - p0).GetNormalized()
        if (-myDir).Dot(thisNormal) >= 0.5:
            selectedPoints.append(polygon.a)
            selectedPoints.append(polygon.b)
            selectedPoints.append(polygon.c)
            selectedPoints.append(polygon.d)
    return selectedPoints

def main():
    global prevMat
    global prevFrame
    global prevObj
    
    myObj = op.GetDown()
    if not myObj: return None
    
    hClone = op.GetAndCheckHierarchyClone(hh, myObj, c4d.HIERARCHYCLONEFLAGS_ASPOLY, False)
    newObj = hClone["clone"]

    curMat = newObj.GetMg()
    scaleFactor = op[c4d.ID_USERDATA,3]
    antiFlicker = op[c4d.ID_USERDATA,1]
    
    if prevMat == None:
        prevMat = curMat
        prevFrame = 0
        
    if prevFrame != (doc.GetTime().GetFrame(doc.GetFps())-1):
        return newObj
    
    vel = curMat.off - prevMat.off
    if vel.GetLength() > antiFlicker:
        vel = c4d.Vector(0)
    myDir = vel.GetNormalized()
    
    pointList = GetPointsOfFace(newObj, myDir)
    for x in range(0, len(pointList)):
        point = newObj.GetPoint(pointList[x])
        point += (-myDir * (vel.GetLength() * scaleFactor))
        newObj.SetPoint(pointList[x], point)
    
    prevMat = curMat
    prevFrame = doc.GetTime().GetFrame(doc.GetFps())
    return newObj
