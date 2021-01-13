from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_Pnt2d
from OCC.Core.BRep import BRep_Tool_Curve
from OCC.Core.GeomLProp import GeomLProp_SLProps
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_Line, GeomAbs_Circle, GeomAbs_Ellipse, GeomAbs_Hyperbola, GeomAbs_Parabola, GeomAbs_BezierCurve, GeomAbs_BSplineCurve, GeomAbs_OffsetCurve, GeomAbs_OtherCurve
from OCC.Core.TopAbs import TopAbs_REVERSED
from OCC.Extend import TopologyUtils
from OCC.Core.TopoDS import TopoDS_Edge
from OCC.Core.GCPnts import GCPnts_AbscissaPoint
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve


class Edge:
    def __init__(self, topods_edge):
        assert isinstance(topods_edge, TopoDS_Edge)
        self._edge = topods_edge
    
    def topods_edge(self):
        return self._edge

    def hash(self):
        return hash(self.topods_edge())
    
    def point(self, u):
        pt = self.curve().Value(u)
        return (pt.X(), pt.Y(), pt.Z())

    def tangent(self, u):
        pt = gp_Pnt()
        der = gp_Vec()
        self.curve().D1(u, pt, der)
        der.Normalize()
        tangent = (der.X(), der.Y(), der.Z())
        if self.reversed():
            tangent = (-tangent[0], -tangent[1], -tangent[2])
        return tangent
    
    def first_derivative(self, u):
        pt = gp_Pnt()
        der = gp_Vec()
        self.curve().D1(u, pt, der)
        return (der.X(), der.Y(), der.Z())

    def length(self, tolerance=1e-9):
        umin, umax = self.u_bounds()
        return GCPnts_AbscissaPoint().Length(BRepAdaptor_Curve(self.topods_edge()), umin, umax, tolerance)

    def curve(self):
        return BRep_Tool_Curve(self._edge)[0]

    def specific_curve(self):
        curv_type = BRepAdaptor_Curve(self._edge).GetType()
        if curv_type == GeomAbs_Line:
            return self.curve().Line()
        if curv_type == GeomAbs_Circle:
            return self.curve().Circle()
        if curv_type == GeomAbs_Ellipse:
            return self.curve().Ellipse()
        if curv_type == GeomAbs_Hyperbola:
            return self.curve().Hyperbola()
        if curv_type == GeomAbs_Parabola:
            return self.curve().Parabola()
        if curv_type == GeomAbs_BezierCurve:
            return self.curve().BezierCurve()
        if curv_type == GeomAbs_BSplineCurve:
            return self.curve().BSplineCurve()
        if curv_type == GeomAbs_OffsetCurve:
            return self.curve().OffsetCurve()
        raise ValueError("Unknown curve type: ", curv_type)


    def u_bounds(self):
        _, umin, umax = BRep_Tool_Curve(self.topods_edge())
        return umin, umax
    
    def twin_edge(self):
        pass

    def convex(self):
        return self.topods_edge().Convex()
    
    def closed(self):
        return self.topods_edge().Closed()

    def reversed(self):
        return self.topods_edge().Orientation() == TopAbs_REVERSED
    
    def curve_type(self):
        curv_type = BRepAdaptor_Curve(self._edge).GetType()
        if curv_type == GeomAbs_Line:
            return "line"
        if curv_type == GeomAbs_Circle:
            return "circle"
        if curv_type == GeomAbs_Ellipse:
            return "ellipse"
        if curv_type == GeomAbs_Hyperbola:
            return "hyperbola"
        if curv_type == GeomAbs_Parabola:
            return "parabola"
        if curv_type == GeomAbs_BezierCurve:
            return "bezier"
        if curv_type == GeomAbs_BSplineCurve:
            return "bspline"
        if curv_type == GeomAbs_OffsetCurve:
            return "offset"
        if curv_type == GeomAbs_OtherCurve:
            return "other"
        return "unknown"
