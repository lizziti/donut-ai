import os
import time
from parse_obj_file import parse_obj_file
from math_utils import rotate_point, project_3d_to_2d, get_face_normal, dot_product, draw_triangle
from ai_generator import generate_3d_model

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 40
FOV = 30
VIEWER_DISTANCE = 30

ASCII_CHARS = ".,-~:;=!*#$@"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    print("Welcome to Donut-AI!")
    user_prompt = input("What would you like to see as 3D ASCII? (e.g. 'a cat'): ")

    model_file = generate_3d_model(user_prompt, "temp_model.obj")

    if not model_file:
        print("Could not generate a model. Exiting.")
        return

    vertices, faces = parse_obj_file(model_file)
    if not vertices:
        return

    sum_x, sum_y, sum_z = 0, 0, 0
    for v in vertices:
        sum_x += v[0]
        sum_y += v[1]
        sum_z += v[2]

    center_x = sum_x / len(vertices)
    center_y = sum_y / len(vertices)
    center_z = sum_z / len(vertices)

    # Scale factor (0.1 reduces the model to 10% of original size)
    SCALE = 0.1

    for i in range(len(vertices)):
        vertices[i][0] = (vertices[i][0] - center_x) * SCALE
        vertices[i][1] = (vertices[i][1] - center_y) * SCALE
        vertices[i][2] = (vertices[i][2] - center_z) * SCALE

    angle_x = 0.0
    angle_y = 0.0
    angle_z = 0.0

    light_vector = [0, 0, -1]

    while True:
        buffer = [[' ' for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
        z_buffer = [[float('inf') for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

        for face in faces:
            p1 = vertices[face[0]]
            p2 = vertices[face[1]]
            p3 = vertices[face[2]]

            r1 = rotate_point(p1[0], p1[1], p1[2], angle_x, angle_y, angle_z)
            r2 = rotate_point(p2[0], p2[1], p2[2], angle_x, angle_y, angle_z)
            r3 = rotate_point(p3[0], p3[1], p3[2], angle_x, angle_y, angle_z)

            normal = get_face_normal(r1, r2, r3)

            luminance = dot_product(normal, light_vector)

            if luminance > 0:
                char_index = int(luminance * (len(ASCII_CHARS) - 1))
                char = ASCII_CHARS[char_index]

                sx1, sy1 = project_3d_to_2d(r1[0], r1[1], r1[2], SCREEN_WIDTH, SCREEN_HEIGHT, FOV, VIEWER_DISTANCE)
                sx2, sy2 = project_3d_to_2d(r2[0], r2[1], r2[2], SCREEN_WIDTH, SCREEN_HEIGHT, FOV, VIEWER_DISTANCE)
                sx3, sy3 = project_3d_to_2d(r3[0], r3[1], r3[2], SCREEN_WIDTH, SCREEN_HEIGHT, FOV, VIEWER_DISTANCE)

                draw_triangle(
                    buffer, z_buffer,
                    int(sx1), int(sy1), r1[2],
                    int(sx2), int(sy2), r2[2],
                    int(sx3), int(sy3), r3[2],
                    char,
                    SCREEN_WIDTH, SCREEN_HEIGHT
                )

        clear_screen()
        for row in buffer:
            print("".join(row))

        angle_x += 0.05
        angle_y += 0.03
        angle_z += 0.01
        time.sleep(0.03)


if __name__ == "__main__":
    main()