from skgeom import *

def visibility(person, obstacles, space, draw_pic = False):
    
    ## object that person could be on
    l   = []
    ## create arrangement
    arr = arrangement.Arrangement()

    ## create space
    outer = [Segment2(Point2(space[i][0], space[i][1]), Point2(space[i+1][0],
                                                               space[i+1][1]))
                      for i in list(range(len(space) - 1))]
    outer.append(Segment2(Point2(space[-1][0], space[-1][1]), Point2(space[0][0],
                                                               space[0][1])))
    
    for s in outer:
        arr.insert(s)
        
    ## create obstacle
    for obstacle in obstacles:
        segments = [Segment2(Point2(obstacle[i][0], obstacle[i][1]), Point2(obstacle[i+1][0],
                                                               obstacle[i+1][1]))
                      for i in list(range(len(obstacle) - 1))]
        segments.append(Segment2(Point2(obstacle[-1][0], obstacle[-1][1]), Point2(obstacle[0][0],
                                                               obstacle[0][1])))
        for s in segments:
            arr.insert(s)
        
        if person in obstacle:
            l.append(obstacle)
            
    ## tricky situation where person is on object
    if l:
        obj  = l[0]
        idx  = obj.index(person)
        if len(obj) == (idx + 1):
            next_idx = 0
        else:
            next_idx = idx + 1
        
        down  = obj[next_idx][1] < obj[idx][1]
        left  = obj[next_idx][0] < obj[idx][0]
        
        person = [person[0], person[1]]
        
        if down:
            person[1] = person[1] + 1e-15 
        else:
            person[1] = person[1] - 1e-15
        
        if left:
            person[0] = person[0] + 1e-15 
        else:
            person[0] = person[0] - 1e-15 
            
    ## create person
    q     = Point2(person[0], person[1])

    ## Making sure person not at the boundary of space
    segment_q = Segment2(q,q)
    bound     = None
    bounds    = []
    point     = None
    space_pts = [Point2(pt[0], pt[1]) for pt in space]
    for segment in outer:
        i = intersection(segment_q, segment)
        if not (i == None):
            bounds.append(segment)
            point  = i
    if len(bounds) > 0:
        try:
            bound = bounds[1] if space_pts.index(point) > 0  else bounds[0]
        except:
            bound = bounds[0]

    if bound is not None:
        idx       = outer.index(bound)
        next_idx  = idx + 1 if not idx == len(space) - 1 else 0
        prev_idx  = idx - 1 if idx > 0 else len(space) - 1
        print(space[idx])
        if (space[prev_idx][1] - space[idx][1]) == 0:
            sig_y = 1 if (space[next_idx][1] - space[idx][1]) > 0 else -1
        else:
            sig_y = 1 if (space[prev_idx][1] - space[idx][1]) > 0 else -1

        if (space[next_idx][0] - space[idx][0]) == 0:
            sig_x = 1 if (space[prev_idx][0] - space[idx][0]) > 0 else -1
        else:
            sig_x = 1 if (space[next_idx][0] - space[idx][0]) > 0 else -1
        q     = Point2(person[0] + sig_x * 1e-15, person[1] + sig_y * 1e-15)

    ## find vision

    face  = arr.find(q)
    vs    = RotationalSweepVisibility(arr)
    vx    = vs.compute_visibility(q, face)
 
    ## compute area
    list_of_points = []
    for v in vx.halfedges:
        list_of_points.append(v.curve().source())

    if draw_pic:
        for he in arr.halfedges:
            draw.draw(he.curve(), visible_point=False)
        for v in vx.halfedges:
            draw.draw(v.curve(), color='red', visible_point=False)
        draw.draw(q, color='magenta')
    
    return Polygon(list_of_points)
    #return Polygon(list_of_points).area()
	
	
a = visibility((10,50), [[(10,10),(20,10), (20,20),(10,20)], [(1,3),(2,3), (5,1),(3,10)],  [(70,30),(80,40), (60,60)]],
           [(100,100), (0,100), (0,0), (100,0)], True)