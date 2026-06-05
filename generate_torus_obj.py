import math


def generate_torus_obj(filename, R=2.0, r=0.8, u_res=30, v_res=15):
    with open(filename, 'w') as f:
        for i in range(u_res):
            u = i * 2 * math.pi / u_res
            for j in range(v_res):
                v = j * 2 * math.pi / v_res

                x = (R + r * math.cos(v)) * math.cos(u)
                y = (R + r * math.cos(v)) * math.sin(u)
                z = r * math.sin(v)

                f.write(f"v {x:.4f} {y:.4f} {z:.4f}\n")

        for i in range(u_res):
            for j in range(v_res):
                next_i = (i + 1) % u_res
                next_j = (j + 1) % v_res

                p1 = i * v_res + j + 1
                p2 = next_i * v_res + j + 1
                p3 = next_i * v_res + next_j + 1
                p4 = i * v_res + next_j + 1

                f.write(f"f {p1} {p2} {p3}\n")
                f.write(f"f {p1} {p3} {p4}\n")


generate_torus_obj("echter_donut.obj")
print("echter_donut.obj wurde erfolgreich erstellt!")