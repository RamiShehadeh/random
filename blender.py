import bpy, math

def make_ribbed_dial(
    name="RibbedDial",
    base_radius=0.1,        # radius of the dial face
    base_height=0.02,       # thickness of the dial
    ridge_height=0.01,      # how far ridges stick out
    num_ridges=32,          # total count of ridges around circumference
    bevel_radius=0.002,     # small bevel on all edges
    bevel_segments=4        # smoothness of that bevel
):
    # 1) Create the dial base
    bpy.ops.mesh.primitive_cylinder_add(
        radius=base_radius,
        depth=base_height,
        location=(0, 0, 0)
    )
    dial = bpy.context.active_object
    dial.name = name + "_Base"

    # 2) Create and position each ridge
    ridges = []
    for i in range(num_ridges):
        angle = 2 * math.pi * i / num_ridges
        # approximate ridge width so they don't overlap
        arc = 2 * math.pi * base_radius / num_ridges * 0.8

        # Make ridge as a cube
        bpy.ops.mesh.primitive_cube_add(size=1)
        ridge = bpy.context.active_object
        ridge.name = f"{name}_Ridge_{i}"

        # Scale cube to a thin bar
        ridge.scale = (
            arc / 2,                         # X-scale = arc length
            (base_height * 1.1) / 2,         # Y-scale = slightly thicker than base
            ridge_height / 2                 # Z-scale = ridge height
        )

        # Move it out to the rim and rotate to face outward
        x = base_radius * math.cos(angle)
        y = base_radius * math.sin(angle)
        ridge.location = (x, y, 0)
        ridge.rotation_euler = (0, 0, angle)

        ridges.append(ridge)

    # 3) Join ridges to the base
    bpy.ops.object.select_all(action='DESELECT')
    dial.select_set(True)
    for r in ridges:
        r.select_set(True)
    bpy.context.view_layer.objects.active = dial
    bpy.ops.object.join()
    dial.name = name

    # 4) Add a small bevel to smooth all edges
    bev = dial.modifiers.new(name="Bevel", type='BEVEL')
    bev.width = bevel_radius
    bev.segments = bevel_segments
    bev.profile = 0.5
    bev.limit_method = 'ANGLE'
    bev.angle_limit = math.radians(30)

    # 5) Smooth-shade the result
    bpy.ops.object.shade_smooth()

    return dial

# — Example usage — #
dial = make_ribbed_dial(
    name="VR_Ribbed_Dial",
    base_radius=0.1,
    base_height=0.02,
    ridge_height=0.008,
    num_ridges=24,
    bevel_radius=0.0015,
    bevel_segments=3
)
