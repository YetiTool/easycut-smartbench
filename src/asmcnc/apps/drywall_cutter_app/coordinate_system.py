'''
Class for handling the various coordinate systems we're using in the dwt app
'''

from asmcnc.comms.logging_system.logging_system import Logger

class CoordinateSystem(object):
    '''Class to store the coordinate system data.'''

    def __init__(self, m):
        self.m = m # Router machine instance
        self.machine_coordinates = self.MachineCoordinates(self.m)
        self.working_coordinates = self.WorkingCoordinates(self.m)
        self.drywall_tec_coordinates = self.DrywallTecCoordinates(self.working_coordinates, self.m)
        self.drywall_tec_laser_coordinates = self.DrywallTecLaserCoordinates(self.drywall_tec_coordinates)

        self.m.s.bind(m_x=lambda i, value: self.log_pos(value))
        self.m.s.bind(m_y=lambda i, value: self.log_pos(value))

    def log_pos(self, value):
        Logger.debug("M: {}, {} W: {}, {} DWT: {}, {} DWTL: {}, {} laser offset: {}, {}".format(
        self.machine_coordinates.get_x(),
            self.machine_coordinates.get_y(),
            self.working_coordinates.get_x(),
            self.working_coordinates.get_y(),
            self.drywall_tec_coordinates.get_x(),
            self.drywall_tec_coordinates.get_y(),
            self.drywall_tec_laser_coordinates.get_x(),
            self.drywall_tec_laser_coordinates.get_y(),
            self.m.laser_offset_x_value,
            self.m.laser_offset_y_value
        ))


    class MachineCoordinates(object):
        '''Class to store the machine coordinates.'''

        def __init__(self, m):
            self.m = m
            self.x = self.m.mpos_x()
            self.y = self.m.mpos_y()
            self.z = self.m.mpos_z()

        def get_x(self):
            return self.m.mpos_x()

        def get_y(self):
            return self.m.mpos_y()

        def get_z(self):
            return self.m.mpos_z()

    class WorkingCoordinates(object):
        '''Class to store the working coordinates.'''

        def __init__(self, m):
            self.m = m
            self.x = m.wpos_x()
            self.y = m.wpos_y()
            self.z = m.wpos_z()

        def get_x(self):
            return self.m.wpos_x()

        def get_y(self):
            return self.m.wpos_y()

        def get_z(self):
            return self.m.wpos_z()

    class DrywallTecCoordinates(object):
        '''Class to store the drywall tec coordinates.'''

        def __init__(self, working_coordinates, m):
            self.m = m
            self.working_coordinates = working_coordinates
            self.x_delta = round(self.m.get_dollar_setting(130)
                            - self.m.limit_switch_safety_distance
                            - self.m.laser_offset_tool_clearance_to_access_edge_of_sheet, 2)
            self.y_delta = round(self.m.get_dollar_setting(131)
                            - self.m.get_dollar_setting(27), 2)
            self.z_delta = 0

            # self.x_delta = self.x_delta * -1
            # self.y_delta = self.y_delta * -1

        def get_x(self):
            return self.working_coordinates.get_x() + self.x_delta

        def get_y(self):
            return self.working_coordinates.get_y() + self.y_delta

        def get_z(self):
            return self.working_coordinates.get_z() + self.z_delta

        def get_mx_from_dwx(self, dw_x):
            """
            Method to get the machine x-coordinate from the drywall tec x-coordinate.

            Parameters:
            dw_x (float): The drywall tec x-coordinate.

            Returns:
            float: The corresponding machine x-coordinate.
            """
            return dw_x - self.x_delta

        def get_my_from_dwy(self, dw_y):
            """
            Method to get the machine y-coordinate from the drywall tec y-coordinate.

            Parameters:
            dw_y (float): The drywall tec y-coordinate.

            Returns:
            float: The corresponding machine y-coordinate.
            """
            return dw_y - self.y_delta

        def get_mz_from_dwz(self, dw_z):
            """
            Method to get the machine z-coordinate from the drywall tec z-coordinate.

            Parameters:
            dw_z (float): The drywall tec z-coordinate.

            Returns:
            float: The corresponding machine z-coordinate.
            """
            return dw_z - self.z_delta

    class DrywallTecLaserCoordinates(object):
        '''Class to store the drywall tec coordinates (using laser as reference).'''

        def __init__(self, dwt_cooridnates):
            self.dwt_coordinates = dwt_cooridnates
            self.laser_delta_x = self.dwt_coordinates.m.laser_offset_x_value
            self.laser_delta_y = self.dwt_coordinates.m.laser_offset_y_value

        def get_x(self):
            return self.dwt_coordinates.get_x() + self.dwt_coordinates.m.laser_offset_x_value

        def get_y(self):
            return self.dwt_coordinates.get_y() + self.dwt_coordinates.m.laser_offset_x_value

        def get_z(self):
            return self.dwt_coordinates.get_z()

        # Methods to get machine coordinates from drywall tec laser coordinates

        def get_mx_from_dwlx(self, dwlx):
            """
            Method to get the machine x-coordinate from the drywall tec laser x-coordinate.

            Parameters:
            dwlx (float): The drywall tec laser x-coordinate.

            Returns:
            float: The corresponding machine x-coordinate.
            """
            return self.dwt_coordinates.get_mx_from_dwx(dwlx - self.laser_delta_x)

        def get_my_from_dwly(self, dwly):
            """
            Method to get the machine y-coordinate from the drywall tec laser y-coordinate.

            Parameters:
            dwly (float): The drywall tec laser y-coordinate.

            Returns:
            float: The corresponding machine y-coordinate.
            """
            return self.dwt_coordinates.get_my_from_dwy(dwly - self.laser_delta_y)

        def get_mz_from_dwlz(self, dwlz):
            """
            Method to get the machine z-coordinate from the drywall tec laser z-coordinate.

            Parameters:
            dwlz (float): The drywall tec laser z-coordinate.

            Returns:
            float: The corresponding machine z-coordinate.
            """
            return self.dwt_coordinates.get_mz_from_dwz(dwlz)