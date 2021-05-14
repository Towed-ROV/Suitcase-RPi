import numpy as np

data_types = {"MTW": "Mean_Temprature_Water",
              "DPT": "depth_beneath_boat",
              "DBT": "depth_beneath_boat",
              "GGA": "GPS_fix_data",
              "GLL": "GPS_Langitude/Logitude",
              "GSV": "Satelites_in_view",
              "HDM": "Heading,_magnetic",
              "HDT": "Heading,_True",
              "LTW": "Distance_traveld_throug_water",
              "MWD": "Wind_direction_and_speed",
              "MWV": "Wind_speed_and_angle",
              "RMC": "GPS_Recomended_Minimum_Navigation_Information",
              "HDG": "Heding_Deviation_and_Variation",
              "RSA": "Rudder_sensor_angle",
              "VHW": "Water_Speed_and_heading",
              "VTG": "Track_made_good_and_ground_speed",
              "VWR": "Relative_wind_speed_and_angle",
              "XDR": "Transducer_values",
              "GSA": "GPS_and_DOP_and_active_satalites",
              "ZDA":
                  "Time_and_Date-_UTC,_d_m_y_local_time_zone",
              "AAM": "Waypoint_Arrival_Alarm",
              "APB": "Autopilot_Sentence_B",
              "XTE": "Measured_cross_track_error",
              "VDM": "Automatic_Information_System_(AIS)",
              "VDO": "Automatic_Information_System_(AIS)",
              "TTM": "Tracked_Target_Message",
              "TLL": "Target_Latitude_and_Longitude",
              "OSD": "Own_Ship_Data",
              "ROS": "GPSGate_Buddy_Position_Update",
              "DSC": "Digital_Selective_Calling_Information",
              "BOD": "Bearing_Origin_to_Destination",
              "RMB": "GPS_Recommended_Minimum_Navigation_Information",
              "WPL": "GPS_Waypoint_Location",
              "RTE": "Routes",
              "DSE": "Extended_Digital_Selective_Calling_Information_including_a_more_accurate_position",
              "VLW": "Distance_Traveled_in_Water"}

data_values = {
    "MTW": ["temprature",
            "Unit",
            "temprature",
            "Unit",
            "temprature",
            "Unit"],
    "DPT": ["depth_beneath_boat",
            "Offsett"],
    "DBT": ["depth_under_boat_in_feet",
            "feet",
            "depth_beneath_boat",
            "meter",
            "depth_under_boat_in_Fathoms",
            "fathoms"],
    "GGA": ["UTC time",
            "latitude",
            "north_or_south",
            "longitude",
            "east_or_west",
            "quality_indicator",
            "satilites_in_use",
            "horsiontal_DOP",
            "Antena_height",
            "Unit",
            "Geoidal separations",
            "Unit",
            "Age_of_differential_data_record",
            "Base_station_id"],
    "GLL": ["Latitude",
            "N or S ",
            "Longitude",
            "E or W",
            "UTC of this position",
            "Status A - Data Valid, V - Data Invalid"],
    "GSV": ["number_of_messages",
            "message_number",
            "satellites_in_view",
            "satellite_number",
            "elevation_degrees",
            "azimuth_degrees_true",
            "SNR_dB_(00-99)",
            "satellite_number",
            "elevation_degrees",
            "azimuth_degrees_true",
            "SNR_dB_(00-99)",
            "satellite_number",
            "elevation_degrees",
            "azimuth_degrees_true",
            "SNR_dB_(00-99)",
            "satellite_number",
            "elevation_degrees",
            "azimuth_degrees_true",
            "SNR_dB_(00-99)",
            "satellite_number",
            "elevation_degrees",
            "azimuth_degrees_true",
            "SNR_dB_(00-99)"],
    "HDM": ["Heading Degrees_magnetic",
            "Unit"],
    "HDT": ["Heading_degrees_True",
            "Unit"],
    "MWV": ["Wind_Angle",
            "R=Relative,T=True",
            "Wind_Speed",
            "Units",
            "A=Valid_V=Invalid"],
    "RMC": ["time",
            "status_V=warning",
            "latitude",
            "north_south",
            "longitude",
            "east_west",
            "velocyty_in_knots",
            "track_made_good_true_deg",
            "date_ddmmyy",
            "magnetic_variation_deg",
            "east_west"],
    "HDG": ["magnetic_sensor_heading_deg",
            "Magnetic_deviation_deg",
            "magnetic_deviation_direction",
            "magnetic_variation_degreees",
            "magnetic_variation_direction"],
    "RSA": ["StarBoard_or_single_rudder_sensor(\"-\"=turn_to_port)",
            "Status_A=valid_V=invalid",
            "port_rudder_sensor",
            "Status_A=valid_V=invalid"],
    "VHW": ["degrees_true",
            "T=true",
            "degrees_mag",
            "Unit",
            "wind_velocity",
            "Unit",
            "wind_velocity",
            "Unit"],
    "VTG": ["track_made_good",
            "Unit",
            "Track_degrees",
            "Unit",
            "track_velocity",
            "Unit",
            "track_velocity",
            "Unit"],
    "VWR": ["wind_direction_degrees",
            "relative_wind_dirrection",
            "wind_velocity",
            "Unit",
            "wind_velocity",
            "Unit",
            "wind_velocity",
            "Unit"],
    "XDR": ["transducer_type",
            "meshurement_data",
            "Units",
            "name_tansducer"],
    "GSA": ["selection_mode",
            "mode",
            "ID_of_1st_satelite",
            "ID_of_2nd_satelite",
            "ID_of_3rd_satelite",
            "ID_of_4th_satelite",
            "ID_of_5th_satelite",
            "ID_of_6th_satelite",
            "ID_of_7th_satelite",
            "ID_of_8th_satelite",
            "ID_of_9th_satelite",
            "ID_of_10th_satelite",
            "ID_of_11th_satelite",
            "ID_of_12th_satelite",
            "PDOP_meters",
            "HDOP_meters",
            "VDOP_meters"],
    "ZDA": ["local_zone_minutes_description",
            "local_zone_description(00_to_+-13h)",
            "year",
            "moth",
            "day",
            "time"],
    "AAM": ["Status_A=Arrival_circle_entered",
            "Status_A=perpendicular_passed_at_waypoint",
            "Arrival_circle_radius",
            "Unit",
            "Waypoint_ID"],
    "RMB": ["Recommended_Minimum_Navigation_Information",
            "Status_A=Active_V=Void",
            "Cross_Track_error_nautical_miles",
            "Direction_to_Steer_Left_or_Right",
            "TO_Waypoint_ID",
            "FROM_Waypoint_ID",
            "Destination_Waypoint_Latitude",
            "N_or_S",
            "Destination_Waypoint_Longitude",
            "E_or_W",
            "Range_to_destination_in_nautical_miles",
            "Bearing_to_destination_in_degrees_True",
            "Destination_closing_velocity_in_knots",
            "Arrival_Status_A=Arrival_Circle_Entered",
            "Status_A_Data_Valid_V_Data_Invalid_FAA_mode_indicator"],
    "WPL": ["Latitude",
            "N_or_S_(North_or_South)",
            "Longitude",
            "E_or_W_(East_or_West)",
            "Waypoint_Name"],
    "RTE": ["Total_number_of_messages_being_transmitted",
            "Message_Number",
            "Message_Mode",
            "c=complete_route_all_waypoints",
            "w=working_route",
            "Waypoint_ID",
            "More_Waypoints"],
    "APB": [
        "Status_V=LORAN-C_Blink_or_SNR_warning_V=general_warning_flag",
        "Status_V=Loran-C_Cycle_Lock_warning_flag_A=OK_or_not_used",
        "Cross_Track_Error_Magnitude",
        "Direction_to_steer_L_or_R",
        "Unit",
        "Status_A=Arrival_Circle_Entered",
        "Status_A=Perpendicular_passed_at_waypoint",
        "Bearing_origin_to_destination",
        "Unit",
        "Destination_Waypoint_ID",
        "Bearing_present_position_to_Destination",
        "Unit",
        "Heading_to_steer_to_destination_waypoint",
        "Unit"],
    "XTE": ["Cross_track_error_measured",
            "General_warning_flag_V=warning",
            "(Loran-C_Blink_or_SNR_warning)",
            "Not_used_for_GPS_(Loran-C_cycle_lock_flag)",
            "Cross_track_error_distance",
            "L_si_Steer_left_to_correct_error_(or_R_for_right)",
            "N-_Distance_Units_Nautical_miles",
            "Status_A_is_Valid_V_is_Invalid"],
    "VDM": ["Time_(UTC)",
            "MMSI_Number",
            "Latitude",
            "Longitude",
            "Speed_in_Knots",
            "Heading",
            "Course_over_Ground",
            "Rate_of_turn",
            "Navigation_status"],
    "VDO": ["Latitude",
            "Longitude",
            "Speed_over_ground",
            "Course_over_ground",
            "MMSI_navigational_status_ship_type_call_sign_destination_sizes_(in_AIS_target_list)"],
    "TTM": ["Target_Number_(0-99)",
            "Target_Distance",
            "Bearing_from_own_ship",
            "Bearing_Units",
            "Target_Speed",
            "Target_Course",
            "Course_Units",
            "Distance_of_closest-point-of-approach",
            "Time_until_closest-point-of-approach_“-”_means_increasing",
            "“-”_means_increasing",
            "Target_name",
            "Target_Status",
            "Reference_Target"],
    "TLL": ["Target_Number_(not_used/ignored)",
            "Latitude",
            "Longitude",
            "Name",
            "Status",
            "Reference_Target_(not_used/ignored)"],
    "OSD": ["Heading_degrees_true",
            "Status_A=Data_Valid",
            "Vessel_Course_degrees_True",
            "Course_Reference",
            "Vessel_Speed",
            "Speed_Reference",
            "Vessel_Set_degrees_True",
            "Vessel_drift(speed)",
            "Units"],
    "ROS": ["Latitude",
            "Hemisphere_N/S",
            "Longitude",
            "Hemisphere_E/W",
            "Altitude_in_meters_above_sea_level",
            "Speed_over_ground_in_knots",
            "Heading_over_ground_in_degrees",
            "Date",
            "Time_UTC",
            "Name_of_buddy_this_position_info_belongs_to.",
            "Notes_CDDSC_and_CDSE._These_standards_are_not_fully_supported_by_Opencpn."],
    "DSC": ["distress_alert_call",
            "the_MMSI_of_the_sender",
            "category",
            "Nature_of_Distress",
            "preferred_follow-on_communication",
            "position_xxxxyyyy_x=lat_y=long",
            "message_sent_time",
            "new_information",
            "signal_in_this_field",
            "S–end_of_sequence",
            "expansion_message_if_E"],
    "DSE": ["total_number_of_datagrams_in_expansion_message",
            "number_of_this_datagram_in_the_message_sequence",
            "unknown(status?)",
            "sender's_MMSI.",
            "see_Table_1_of_ITU-Rec",
            "data_payload"],
    "MDA": ["Barometric_pressure_inches_of_mercury",
            "Barometric_pressure_bars",
            "Air_temperature_degrees_C",
            "Water_temperature_degrees_C",
            "Water_temperature_degrees_C",
            "Relative_humidity_percent",
            "Absolute_humidity_percent_Dew_point_degrees_C",
            "Wind_direction_degrees_True_",
            "Wind_direction_degrees_Magnetic_Wind_speed_knots"],
    "VLW": ["water_distance_traveled",
            "Unit",
            "water_distance_since_reset",
            "Unit",
            "ground_distance_traveld",
            "Unit",
            "ground_distance_since_reset",
            "Unit"]}

CONDITIONS = {"depth_under_boat": lambda v: -1 if v is None else v,
              "depth_under_boat_in_Fathoms": lambda v: -1 if v is None else v,
              "depth_under_boat_in_feet": lambda v: -1 if v is None else v,
              "depth_under_transuducer": lambda v: -1 if v is None else v, }


def get_data_type(identifier):
    """
    gets the data type of an NMEA string, given the identifier, the method returns a more human readable version of that string.
    :param identifier:
    :return:
    """
    if identifier in data_types:
        return data_types[identifier]
    else:
        return "%s: %s \n" % ("unknow ID", identifier)


def set_spesial_conditions(msg):
    """
    loads any contitions set int the nmea utils module, this function calls a lambda function. it is dependent on
    the system. for example, the depth can be set to -1 instead of None. t
    :param msg: the msg to set the contition off
    :return: the returned message.
    """
    for key, condition in CONDITIONS.items():
        if key in msg:
            msg[key] = condition(msg[key])
            if msg[key] is None:
                print("found none")

    return msg


def get_unit_indecies(ordered_data, data_id, data):
    """
    gets points in nmea data that has the Unit clarifiacton, if it has, it is removed, and is added to the sensor.
    in a normal nmea message it will change from for example Depth to depth_in_meters
    :param ordered_data: a list of values that we want to add indicise to.
    :param data_id: the id of the data.
    :param data: the data to check
    :return:
    """
    if data_id in data_values.keys():
        if "Unit" in data_values[data_id]:
            data_structure = data_values[data_id].copy()
            if len(data_structure) > len(data):
                data_structure = data_structure[0:len(data)]
            print(data_structure, data_id, data)
            indexis = np.array([i for i, s in enumerate(data_structure) if s == "Unit"])
            print(indexis, len(data))
            indexis = indexis[0:len(data) - 1]
            print(indexis, len(data))
            for i in indexis[::-1]:
                s = "%s_in_%s" % (data_values[data_id][i - 1], data.pop(i))
                ordered_data[s] = data.pop(i - 1)
    return ordered_data, data_id, data


def add_names(ordered_data, data_id, data):
    """
    adds readable names to NMEA data.
    :param ordered_data: the data we want to build.
    :param data_id: the id of the nmea data.
    :param data: the data we are building from.
    :return:
    """
    for i, value in enumerate(data):
        if data_id in data_values.keys() and i < len(data_values[data_id]):
            ordered_data[data_values[data_id][i]] = value
        else:
            ordered_data["%s_value_%s" %(data_id, i)] = value
    return ordered_data
