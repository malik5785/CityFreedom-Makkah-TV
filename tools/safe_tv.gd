extends Spatial
# Safe TV mode: bounded procedural demo, no full V11 startup, audio, network or heavy assets.
var player
var cam
var speed = 8.0
var status
var elapsed = 0.0

func _ready():
    var env_node = WorldEnvironment.new()
    var env = Environment.new()
    env.background_mode = Environment.BG_COLOR
    env.background_color = Color(0.52, 0.72, 0.88)
    env.ambient_light_color = Color(0.9, 0.9, 0.85)
    env.ambient_light_energy = 0.8
    env_node.environment = env
    add_child(env_node)
    var sun = DirectionalLight.new()
    sun.rotation_degrees = Vector3(-55, -25, 0)
    sun.light_energy = 0.8
    add_child(sun)
    var ground = MeshInstance.new()
    var gm = CubeMesh.new()
    gm.size = Vector3(120, 0.5, 120)
    ground.mesh = gm
    ground.material_override = _material(Color(0.77, 0.69, 0.54))
    add_child(ground)
    for i in range(24):
        var building = MeshInstance.new()
        var mesh = CubeMesh.new()
        var h = 3.0 + float((i * 7) % 13)
        mesh.size = Vector3(5, h, 6)
        building.mesh = mesh
        building.translation = Vector3(float((i % 6) - 3) * 13 + 6, h * 0.5, float(int(i / 6) - 2) * 19)
        building.material_override = _material(Color(0.75, 0.72, 0.65) if i % 2 == 0 else Color(0.89, 0.84, 0.73))
        add_child(building)
    player = Spatial.new()
    player.translation = Vector3(0, 1.5, 16)
    add_child(player)
    cam = Camera.new()
    cam.current = true
    cam.far = 180
    cam.translation = Vector3(0, 5, 13)
    add_child(cam)
    cam.look_at(player.translation + Vector3(0, 0, -12), Vector3.UP)
    var ui = CanvasLayer.new()
    add_child(ui)
    status = Label.new()
    status.text = "CITY FREEDOM - SAFE TV MODE | D-pad: move | 24 buildings"
    status.rect_position = Vector2(24, 24)
    status.add_color_override("font_color", Color(1, 1, 1))
    ui.add_child(status)
    set_process(true)

func _material(c):
    var mat = SpatialMaterial.new()
    mat.albedo_color = c
    mat.flags_unshaded = true
    return mat

func _process(delta):
    elapsed += delta
    var motion = Vector3()
    if Input.is_action_pressed("ui_left"):
        motion.x -= 1
    if Input.is_action_pressed("ui_right"):
        motion.x += 1
    if Input.is_action_pressed("ui_up"):
        motion.z -= 1
    if Input.is_action_pressed("ui_down"):
        motion.z += 1
    if motion.length() > 0:
        player.translation += motion.normalized() * speed * delta
        player.translation.x = clamp(player.translation.x, -45, 45)
        player.translation.z = clamp(player.translation.z, -45, 45)
    cam.translation = player.translation + Vector3(0, 5, 13)
    cam.look_at(player.translation + Vector3(0, 0, -12), Vector3.UP)
    if int(elapsed) % 2 == 0:
        status.text = "CITY FREEDOM SAFE TV | RUNNING %ds | D-pad move" % int(elapsed)
