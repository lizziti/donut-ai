import math

def rotate_point(x, y, z, angle_x, angle_y, angle_z):
    # 1. Rotation around X-axis
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y1 = y * cos_x - z * sin_x
    z1 = y * sin_x + z * cos_x
    x1 = x

    # 2. Rotation around Y-axis
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x2 = x1 * cos_y + z1 * sin_y
    y2 = y1
    z2 = -x1 * sin_y + z1 * cos_y

    # 3. Rotation around Z-axis
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
    x3 = x2 * cos_z - y2 * sin_z
    y3 = x2 * sin_z + y2 * cos_z
    z3 = z2

    return [x3, y3, z3]


def project_3d_to_2d(x, y, z, screen_width, screen_height, fov, viewer_distance):
    factor = fov / (viewer_distance + z)

    x_proj = x * factor * 2
    y_proj = y * factor

    x_screen = int(screen_width / 2 + x_proj)

    y_screen = int(screen_height / 2 - y_proj)

    return x_screen, y_screen


def get_face_normal(p1, p2, p3):
    ux, uy, uz = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
    vx, vy, vz = p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]

    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx

    length = math.sqrt(nx * nx + ny * ny + nz * nz)
    if length == 0:
        return 0, 0, 0

    return nx / length, ny / length, nz / length


def dot_product(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]


def draw_triangle(buffer, z_buffer, x1, y1, z1, x2, y2, z2, x3, y3, z3, char, screen_width, screen_height):
    min_x = max(0, min(x1, x2, x3))
    max_x = min(screen_width - 1, max(x1, x2, x3))
    min_y = max(0, min(y1, y2, y3))
    max_y = min(screen_height - 1, max(y1, y2, y3))

    def edge_function(ax, ay, bx, by, px, py):
        return (px - ax) * (by - ay) - (py - ay) * (bx - ax)

    area = edge_function(x1, y1, x2, y2, x3, y3)

    if area == 0:
        return

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            w0 = edge_function(x2, y2, x3, y3, x, y)
            w1 = edge_function(x3, y3, x1, y1, x, y)
            w2 = edge_function(x1, y1, x2, y2, x, y)

            if (w0 >= 0 and w1 >= 0 and w2 >= 0) or (w0 <= 0 and w1 <= 0 and w2 <= 0):

                alpha = w0 / area
                beta = w1 / area
                gamma = w2 / area

                z_pixel = alpha * z1 + beta * z2 + gamma * z3

                if z_pixel < z_buffer[y][x]:
                    z_buffer[y][x] = z_pixel
                    buffer[y][x] = char