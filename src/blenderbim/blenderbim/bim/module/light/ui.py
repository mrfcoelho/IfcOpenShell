# BlenderBIM Add-on - OpenBIM Blender Add-on
# Copyright (C) 2020, 2021 Dion Moult <dion@thinkmoult.com>
#
# This file is part of BlenderBIM Add-on.
#
# BlenderBIM Add-on is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlenderBIM Add-on is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BlenderBIM Add-on.  If not, see <http://www.gnu.org/licenses/>.

import bpy
from blenderbim.bim.module.light.data import SolarData
from sun_position.sun_calc import format_time, format_hms, sun


class BIM_PT_radiance_exporter(bpy.types.Panel):
    """Creates a Panel in the render properties window"""
    bl_label = "Radiance Exporter"
    bl_idname = "BIM_PT_radiance_exporter"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_parent_id = "BIM_PT_tab_services"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        props = scene.radiance_exporter_properties
        
        row = layout.row()
        row.prop(props, "ifc_file_name")

        row = layout.row()
        row.prop(props, "json_file_path")
        
        row = layout.row()
        row.label(text="Resolution")
        row.prop(props, "radiance_resolution_x", text="X")
        
        row = layout.row()
        row.label(text="")
        row.prop(props, "radiance_resolution_y", text="Y")
        
        row = layout.row()
        row.prop(props, "radiance_quality")
        
        row = layout.row()
        row.prop(props, "radiance_detail")
        
        row = layout.row()
        row.prop(props, "radiance_variability")
        
        row = layout.row()
        row.operator("export_scene.radiance", text="Export to OBJ")

        row = layout.row()
        row.operator("render_scene.radiance", text="Radiance Render")


class BIM_PT_solar(bpy.types.Panel):
    """Creates a Panel in the render properties window"""
    bl_label = "Solar Access / Shadow"
    bl_idname = "BIM_PT_solar"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_parent_id = "BIM_PT_tab_solar_analysis"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        if not SolarData.is_loaded:
            SolarData.load()

        props = context.scene.BIMSolarProperties

        if SolarData.data["sites"]:
            row = self.layout.row(align=True)
            row.prop(props, "sites")
            row.operator("bim.import_lat_long", icon="IMPORT", text="")
        else:
            row = self.layout.row(align=True)
            row.label(text="No Sites With Lat/Longs Found", icon="ERROR")

        sun_props = context.scene.sun_pos_properties

        row = self.layout.row()
        row.prop(sun_props, "coordinates", icon='URL')
        row = self.layout.row(align=True)
        row.prop(props, "latitude")
        row.prop(props, "longitude")

        row = self.layout.row(align=True)
        row.prop(props, "true_north")
        if SolarData.data["true_north"] is not None:
            row.operator("bim.import_true_north", icon="IMPORT", text="")

        row = self.layout.row(align=True)
        row.prop(props, "month", text={
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }[props.month])
        row.prop(props, "day")

        row = self.layout.row(align=True)
        row.prop(props, "hour")
        row.prop(props, "minute")

        col = self.layout.column(align=True)
        box = col.box()
        row = box.row()
        row.alignment = "CENTER"
        row.label(text=props.timezone)

        row = col.row(align=True)
        box = row.box()

        local_time = format_time(sun_props.time, sun_props.use_daylight_savings)
        utc_time = format_time(sun_props.time, sun_props.use_daylight_savings, sun_props.UTC_zone)

        row2 = box.row()
        row2.label(text=f"Local Time: {local_time}")
        row2 = box.row()
        row2.label(text=f"UTC Time: {utc_time}")

        box = row.box()

        sunrise = format_hms(sun.sunrise)
        sunset = format_hms(sun.sunset)

        row2 = box.row()
        row2.label(text=f"Sunrise: {sunrise}")
        row2 = box.row()
        row2.label(text=f"Sunset: {sunset}")

        col = self.layout.column(align=True)
        row = col.row(align=True)
        row.prop(props, "display_sun_path", icon="LIGHT_SUN")
        row.prop(props, "sun_path_size")

        if props.display_sun_path:
            row = col.row()
            row.operator("bim.move_sun_path_to_3d_cursor")

        row = self.layout.row(align=True)
        row.prop(props, "display_shadows", icon="SHADING_RENDERED")
        row.prop(context.scene.display.shading, "shadow_intensity", text="Shadow Intensity")

        row = self.layout.row(align=True)
        row.operator("bim.view_from_sun", icon="LIGHT_HEMI")
