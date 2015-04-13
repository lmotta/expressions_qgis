"""
/***************************************************************************
Name                 : IBAMA expressions
Description          : Set of expressions for QGIS ( 2.8 or above )
Date                 : April, 2015.
copyright            : (C) 2015 by Luiz Motta
email                : motta.luiz@gmail.com

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import ( qgsfunction )
#from qgis.gui import *

from PyQt4.QtCore import ( QDate, QFileInfo )

# //////// Inline Functions \\\\\\\\

def dms_format(dd, orients):
  def decdeg2dms(dd):
   minutes, seconds = divmod( abs( dd ) * 3600, 60 )
   degrees, minutes = divmod( minutes, 60 )
   return { 'orient': dd >= 0.0, 'degrees': degrees, 'minutes': minutes, 'seconds': seconds }
  def formatDMS(dms):
    ( d, m, s, o ) = ( "%02.0f" % dms['degrees'], "%02.0f" % dms['minutes'], " %05.2f" % dms['seconds'], orients[ dms['orient'] ] )
    return "%s%s %s%s %s%s %s" % (  d, chr(176), m, chr(39), s, chr(34), o )
  #
  return formatDMS( decdeg2dms( dd ) )

# \\\\\\\\ Inline Functions ////////

@qgsfunction(args=1, group='Ibama')
def getNameFile(values, feature, parent):
  """
  <h4>Return</h4>Only name of file whithout extension
  <p><h4>Syntax</h4>getNameFile(path_file)</p>
  <p><h4>Argument</h4>path_file -> name file with path</p>
  <p><h4>Example</h4>getNameFile('/home/user/readme.txt')-> readme</p>
  <p>* Change the '/' for your system (this example is for Linux)</p>
  """
  try:
    info = QFileInfo( values[0] )
    name = info.baseName()
  except:
    raise Exception("Enter with name of file.")
    return ''
  #
  return name

@qgsfunction(0, "Ibama")
def dms_x(values, feature, parent):
  """
  <h4>Return</h4>Coordinate X of geometry D M S Q(W or E)
    <p> Point: Coordinate own</p>
    <p> Line: Coordinate of center</p>
    <p> Polygon: Coordinate of centroid</p>
  <p><h4>Syntax</h4>$dms_x</p>
  """
  geom = feature.geometry()
  if geom is None:
    return 'No Geometry'
  point = geom.centroid().asPoint()
  orients = {True: 'E', False: 'W'}
  return dms_format( point.x(), orients )

@qgsfunction(0, "Ibama")
def dms_y(values, feature, parent):
  """
  <h4>Return</h4>Coordinate Y of geometry D M S Q(N or S)
    <p> Point: Coordinate own</p>
    <p> Line: Coordinate of center</p>
    <p> Polygon: Coordinate of centroid</p>
  <p><h4>Syntax</h4>$dms_x</p>
  """
  geom = feature.geometry()
  if geom is None:
    return 'No Geometry'
  point = geom.centroid().asPoint()
  orients = {True: 'N', False: 'S'}
  return dms_format( point.y(), orients )

@qgsfunction(1, "Ibama")
def existFile(values, feature, parent):
  """
  <h4>Return</h4>True if exist and False otherwise
  <p><h4>Syntax</h4>existFile(v_file)</p>
  <p><h4>Argument</h4>v_file-> file with path</p>
  <p><h4>Example</h4>existFile( '/home/not_exist.txt')-> False</p>
  <p>* Change the '/' for your system (this example is for Linux)</p>
  """
  try:
    info = QFileInfo( values[0] )
    exist = info.isFile()
  except:
    raise Exception("Enter with file with path")
    return None
  #
  return exist

@qgsfunction(1, "Ibama")
def getDateLandsat(values, feature, parent):
  """
  <h4>Return</h4>QDate from file name of Landsat
  <p><h4>Syntax</h4>getDateLandsat(name_landsat)</p>
  <p><h4>Argument</h4>name_landsat -> name file of Landsat</p>
  <p><h4>Example</h4>getDateLandsat('LC81390452014295LGN00')-> QDate(2014, 10, 22)</p>
  """
  try:
    julianYear = QDate( int( values[0][9:13] ), 1, 1 ).toJulianDay() - 1
    julianDays = julianYear + int( values[0][13:16] )
    v_date = QDate.fromJulianDay ( julianDays )
  except:
    raise Exception("Enter with landsat 8 name (ex. 'LC81390452014295LGN00').")
    return QDate()
  #
  return v_date
