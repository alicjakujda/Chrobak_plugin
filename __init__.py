# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TestChrob
                                 A QGIS plugin
 Testing plugin
                             -------------------
        begin                : 2018-05-01
        copyright            : (C) 2018 by Alicja Kujda
        email                : alicjakujda@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load TestChrob class from file TestChrob.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .TestChrobModule import TestChrob
    return TestChrob(iface)
