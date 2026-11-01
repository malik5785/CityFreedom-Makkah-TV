#!/usr/bin/env python3
"""Mechanical first pass of the ORIGINAL V11 Godot 4 script into Godot 3.6.
This does not claim semantic equivalence; Godot 3 parser must validate output."""
from pathlib import Path
import re
source=Path("original_v11_reference/main.gd").read_text(encoding="utf-8")
replacements={
"BaseMaterial3D":"SpatialMaterial","CharacterBody3D":"KinematicBody","Node3D":"Spatial","Camera3D":"Camera",
"DirectionalLight3D":"DirectionalLight","OmniLight3D":"OmniLight",
"MeshInstance3D":"MeshInstance","StandardMaterial3D":"SpatialMaterial",
"ProceduralSkyMaterial":"ProceduralSky","BoxShape3D":"BoxShape",
"SphereShape3D":"SphereShape","CylinderShape3D":"CylinderShape",
"CollisionShape3D":"CollisionShape","StaticBody3D":"StaticBody",
"RayCast3D":"RayCast","AudioStreamPlayer3D":"AudioStreamPlayer3D",
"Transform3D":"Transform","Basis.IDENTITY":"Basis()",
"Vector2i":"Vector2","PackedVector3Array":"PoolVector3Array",
"PackedVector2Array":"PoolVector2Array","PackedColorArray":"PoolColorArray",
"PackedInt32Array":"PoolIntArray","PackedFloat32Array":"PoolRealArray",
"PackedStringArray":"PoolStringArray","Color.WHITE":"Color(1,1,1)",
"Color.BLACK":"Color(0,0,0)","Color.TRANSPARENT":"Color(0,0,0,0)",
"Vector3.UP":"Vector3(0,1,0)","Vector3.ZERO":"Vector3(0,0,0)",
"Vector2.ZERO":"Vector2(0,0)","Mesh.PRIMITIVE_TRIANGLES":"Mesh.PRIMITIVE_TRIANGLES",
"InputEventKey.keycode":"InputEventKey.scancode",
"emission_energy_multiplier":"emission_energy",
"clampf(":"clamp(","absf(":"abs(","mini(":"min(","maxi(":"max(",
"randf_range(":"rand_range(","randi_range(":"randi_range(",
}
for old,new in replacements.items():
    source=source.replace(old,new)
# Godot 3 does not support inline anonymous function expressions.
source=source.replace('spots.sort_custom(func(x, y): return (x[0] as Vector2).distance_squared_to(start_pos) < (y[0] as Vector2).distance_squared_to(start_pos))', 'spots.sort_custom(self, "_sort_spots_by_distance")')
source=source.replace('list.sort_custom(func(x, y): return x[0] < y[0])', 'list.sort_custom(self, "_sort_district_distance")')
source += '\nfunc _sort_district_distance(x, y):\n    return x[0] < y[0]\n'
source += '\nfunc _sort_spots_by_distance(x, y):\n    return x[0].distance_squared_to(start_pos) < y[0].distance_squared_to(start_pos)\n'
source=source.replace('best.sort_custom(func(a, b): return a[0] < b[0])', 'best.sort_custom(self, "_sort_district_distance")')
# Godot 3 Basis has no static looking_at constructor; use Transform.looking_at.
source=source.replace('Transform(Basis.looking_at(-sun_dir, Vector3.UP), Vector3.ZERO)', 'Transform().looking_at(-sun_dir, Vector3.UP)')
source=source.replace('Transform(Basis.looking_at(-moon_dir, Vector3.UP), Vector3.ZERO)', 'Transform().looking_at(-moon_dir, Vector3.UP)')
# Replace after all class and vector constants have been renamed.
source=re.sub(r'Transform\\(Basis\\.looking_at\\((-?\\w+),\\s*Vector3\\(0,1,0\\)\\),\\s*Vector3\\(0,0,0\\)\\)', r'Transform().looking_at(\\1, Vector3(0,1,0))', source)
# Godot 3 Transform.looking_at accepts target point and up vector.
source=re.sub(r'Transform\\(Basis\\.looking_at\\(([^,]+),\\s*Vector3\\(0,1,0\\)\\),\\s*Vector3\\(0,0,0\\)\\)', r'Transform().looking_at(\\1, Vector3(0,1,0))', source)
source=source.replace('Transform(Basis.looking_at(-sun_dir, Vector3(0,1,0)), Vector3(0,0,0))', 'Transform().looking_at(-sun_dir, Vector3(0,1,0))')
source=source.replace('Transform(Basis.looking_at(-moon_dir, Vector3(0,1,0)), Vector3(0,0,0))', 'Transform().looking_at(-moon_dir, Vector3(0,1,0))')
if 'Basis.looking_at' in source:
    raise RuntimeError('Unconverted Basis.looking_at: ' + source[source.index('Basis.looking_at')-55:source.index('Basis.looking_at')+95])
# Remove typed declarations and return annotations; leave original functions and control flow.
source=re.sub(r'(?m)^(\s*(?:var|const)\s+\w+)\s*:\s*[A-Za-z_][A-Za-z_0-9]*(?=\s*(?:=|$))',r'\1',source)
source=re.sub(r'(?m)^(\s*func\s+\w+\([^\n]*?\))\s*->\s*[A-Za-z_][A-Za-z_0-9]*\s*:',r'\1:',source)
source=re.sub(r'\b([A-Za-z_]\w*)\s*:\s*(?:float|int|bool|String|Vector2|Vector3|Color|Array|Dictionary|Node|Spatial|Control|Label|Mesh|Transform|Basis|KinematicBody|InputEvent|AudioStreamWAV)(?=\s*[,)=])',r'\1',source)
source=re.sub(r'\bvar\s+(\w+)\s*:=',r'var \1 =',source)
source=re.sub(r'\bconst\s+(\w+)\s*:=',r'const \1 =',source)
source=source.replace('get_viewport().size_changed.connect(_resize_ui)','get_viewport().connect("size_changed", self, "_resize_ui")')
source=source.replace("Color.html(", "Color(")
source=source.replace('Time.get_ticks_msec()','OS.get_ticks_msec()')
source=source.replace('Time.get_ticks_usec()','OS.get_ticks_usec()')
source=source.replace('deg_to_rad(','deg2rad(').replace('rad_to_deg(','rad2deg(')
source=source.replace('lerpf(','lerp(').replace('snappedf(','stepify(')
source=source.replace('.instantiate()','.instance()')
source=source.replace('queue_redraw()','update()')
source=source.replace('draw_string(font,','draw_string(font,')
Path("godot3").mkdir(exist_ok=True)
Path("godot3/main.gd").write_text(source,encoding="utf-8")
Path("godot3/main.tscn").write_text('[gd_scene load_steps=2 format=2]\n[ext_resource path="res://main.gd" type="Script" id=1]\n[node name="CityFreedomMakkah" type="Spatial"]\nscript = ExtResource( 1 )\n')
Path("godot3/project.godot").write_text('config_version=4\n[application]\nconfig/name="City Freedom Makkah V11 TV"\nrun/main_scene="res://main.tscn"\n[rendering]\nquality/driver/driver_name="GLES2"\n')
print(f"Converted first-pass original V11: {len(source)} bytes")
