class Point(object):
    next_id = 0
    def __init__(self, 
                 x, 
                 y, 
                 z):
        self.id = Point.next_id
        Point.next_id = Point.next_id + 1
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    def __cmp__(self, other):
        if self.id < other.id:
            return -1
        elif self.id == other.id:
            return 0
        else:
            return 1

    def translate(self, x=0, y=0, z=0):
        return Point(self.x + x,
                     self.y + y,
                     self.z + z)

    def __str__(self):
        # Convert to meters
        return "    (%s %s %s) // Vertex %s" % (self.x/1000.0, self.y/1000.0, self.z/1000.0, self.id)

class Face(object):
    def __init__(self, conn):
        self.connectivity = conn

    def __str__(self):
        conn = ''.join([str(vrt) + ' '  for vrt in self.connectivity])
        return "        (%s)" % (conn,)

class Patch(object):
    def __init__(self, type, name, faces):
        self.type = type
        self.name = name
        self.faces = faces

    def __str__(self):
        s = "    %s %s\n" % (self.type, self.name)
        s = s + "    (\n"
        for face in self.faces:
            s = s + "%s\n" % (face,)
        s = s + "    )\n"
        return s

class Cell(object):
    def __init__(self, 
                 connectivity, 
                 nx, 
                 ny, 
                 nz, 
                 grad_x = 1, 
                 grad_y = 1, 
                 grad_z = 1):
        self.id = id
        self.connectivity = connectivity
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.grad_x = grad_x
        self.grad_y = grad_y
        self.grad_z = grad_z
        self.f0 = Face([connectivity[0],
                        connectivity[3],
                        connectivity[2],
                        connectivity[1]])
        self.f1 = Face([connectivity[4],
                        connectivity[5],
                        connectivity[6],
                        connectivity[7]])
        self.f2 = Face([connectivity[0],
                        connectivity[1],
                        connectivity[5],
                        connectivity[4]])
        self.f3 = Face([connectivity[1],
                        connectivity[2],
                        connectivity[6],
                        connectivity[5]])
        self.f4 = Face([connectivity[2],
                        connectivity[3],
                        connectivity[7],
                        connectivity[6]])
        self.f5 = Face([connectivity[0],
                        connectivity[4],
                        connectivity[7],
                        connectivity[3]])

    def __cmp__(self, other):
        if self.id < other.id:
            return -1
        elif self.id == other.id:
            return 0
        else:
            return 1

    def __str__(self):
        conn = ''.join([str(vrt) + ' '  for vrt in self.connectivity])
        return "    hex ( %s ) (%s %s %s) simpleGrading (%s %s %s)" % \
                         (conn, self.nx, self.ny, self.nz, self.grad_x, self.grad_y, self.grad_z)
points = []
cells = []
patches = []

if __name__ == '__main__':
    pnts = [Point(-304.8, 0, -300),
            Point(0, 0, -300),
            Point(12, 0, -300),
            Point(14, 0, -300),
            Point(22, 0, -300),
            Point(30, 0, -300),
            Point(38, 0, -300),
            Point(338, 0, -300)]
    points.extend(pnts)
    for z_coord in [300, 302, 307.5, 315, 326, 339, 639]:
        for pnt in pnts[:]:
            points.append(pnt.translate(z=z_coord))
    for pnt in points[:]:
        points.append(pnt.translate(y=10.0))
    nx = {0:100,
          1:12,
          2:2,
          3:8,
          4:8,
          5:8,
          6:100}
    nz = {0:100,
          1:2,
          2:3,
          3:2,
          4:3,
          5:2,
          6:100}
    for z_layer in range(7):
        for x_layer in range(7):
            conn = [z_layer*8 + x_layer,
                    z_layer*8 + 1 + x_layer,
                    z_layer*8 + 1 + 64 + x_layer,
                    z_layer*8 + 64 + x_layer,
                    (z_layer + 1)*8 + x_layer,
                    (z_layer + 1)*8 + 1 + x_layer,
                    (z_layer + 1)*8 + 1 + 64 + x_layer,
                    (z_layer + 1)*8 + 64 + x_layer]
            cell = Cell(conn, nx[x_layer], 1, nz[z_layer])
            cells.append(cell)
    # Delete the adiabatic blocks
    del cells[29]
    del cells[28]
    del cells[22]
    del cells[21]
    del cells[15]
    del cells[14]
    patches.append(Patch(type="symmetryPlane",
                         name = "left",
                         faces = [cells[0].f5,
                                  cells[7].f5,
                                  cells[29].f5,
                                  cells[36].f5]))
    patches.append(Patch(type="patch",
                         name = "right",
                         faces = [cells[6].f3,
                                  cells[13].f3,
                                  cells[18].f3,
                                  cells[23].f3,
                                  cells[28].f3,
                                  cells[35].f3,
                                  cells[42].f3]))
    patches.append(Patch(type="patch",
                         name = "inlet",
                         faces = [cells[0].f0,
                                  cells[1].f0,
                                  cells[2].f0,
                                  cells[3].f0,
                                  cells[4].f0,
                                  cells[5].f0,
                                  cells[6].f0]))
    patches.append(Patch(type="patch",
                         name = "outlet",
                         faces = [cells[36].f1,
                                  cells[37].f1,
                                  cells[38].f1,
                                  cells[39].f1,
                                  cells[40].f1,
                                  cells[41].f1,
                                  cells[42].f1]))
    patches.append(Patch(type="wall",
                         name = "bottom",
                         faces = [cells[7].f1,]))
    patches.append(Patch(type="wall",
                         name = "top",
                         faces = [cells[29].f0,]))
    patches.append(Patch(type="patch",
                         name = "applied",
                         faces = [cells[14].f5,
                                  cells[19].f5,
                                  cells[24].f5]))
    patches.append(Patch(type="patch",
                         name = "adiabatic",
                         faces = [cells[8].f1,
                                  cells[30].f0]))
    front = []
    back = []
    for cell in cells:
        front.append(cell.f2)
        back.append(cell.f4)
    patches.append(Patch(type="empty",
                         name = "front",
                         faces = front))
    patches.append(Patch(type="empty",
                         name = "back",
                         faces = back))
    print("vertices\n(")
    for pnt in points:
        print(pnt)
    print(");")
    print("blocks\n(")
    for index, cell in enumerate(cells):
        print(str(cell) + "// block %s" % (index))
    print(");")
    print("edges\n(\n);")
    print("patches\n(")
    for patch in patches:
        print(patch)
    print(");")