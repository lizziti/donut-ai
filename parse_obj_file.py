def parse_obj_file(file_path):
    vertices = []
    faces = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.split('#')[0]
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                parts = line.split()
                prefix = parts[0]

                if prefix == 'v':
                    x = float(parts[1])
                    y = float(parts[2])
                    z = float(parts[3])
                    vertices.append([x, y, z])

                elif prefix == 'f':
                    face_indices = []
                    for part in parts[1:]:
                        vertex_index = int(part.split('/')[0])
                        face_indices.append(vertex_index - 1)
                    faces.append(face_indices)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None, None

    return vertices, faces