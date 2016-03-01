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

@qgsfunction(0, "Ibama", usesgeometry=True)
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

@qgsfunction(0, "Ibama", usesgeometry=True)
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

def getDateRapideye(values, feature, parent):
  """
  <h4>Return</h4>QDate from file name of Rapideye
  <p><h4>Syntax</h4>getDateRapideye(name_rapideye)</p>
  <p><h4>Argument</h4>name_rapideye -> name file of Rapideye</p>
  <p><h4>Example</h4>getDateRapideye('2227625_2012-12-26T142009_RE1_3A-NAC_14473192_171826')-> QDate(2012, 12, 26)</p>
  """
  try:
    v_date = QDate.fromString( values[0].split('_')[1][:10], "yyyy-MM-dd" )
  except:
    raise Exception("Enter with Rapideye name (ex. '2227625_2012-12-26T142009_RE1_3A-NAC_14473192_171826'). Value error = %s" % values[0])
    return QDate()
  #
  return v_date
  
@qgsfunction(args=1, group="Ibama")
def getDateSentinel(values, feature, parent):
  """
  <h4>Return</h4>QDate from file name of Sentinel
  <p><h4>Syntax</h4>getDateRapideye(name_sentinel)</p>
  <p><h4>Argument</h4>name_sentinel -> name file of Sentinel</p>
  <p><h4>Example</h4>getDateSentinel('s1a-ew-grd-hh-20141031t223708-20141031t223811-003079-003869-001')-> QDate(2014, 10, 31)</p>
  """
  try:
    v_date = QDate.fromString( values[0].split('-')[5][:8], "yyyyMMdd" )
  except:
    raise Exception("Enter with Sentinel name (ex. 's1a-ew-grd-hh-20141031t223708-20141031t223811-003079-003869-001'). Value error = %s" % values[0])
    return QDate()
  #
  return v_date

@qgsfunction(args=0, group="Ibama")
def num_geoms(values, feature, parent):
  """
  <h4>Return</h4>Number of geoms
  <p><h4>Syntax</h4>num_geoms()</p>
  """
  geom = feature.geometry()
  if geom is None or not geom.isGeosValid():
    return -1
  if not geom.isMultipart():
    return 1
  wkbType = geom.wkbType()
  if wkbType == QGis.WKBMultiPoint:
    return len( geom.asMultiPoint() )
  if wkbType == QGis.WKBMultiLineString:
    return len( geom.asMultiPolyline() ) 
  if wkbType == QGis.WKBMultiPolygon:
    return len( geom.asMultiPolygon() ) 

  return -1

@qgsfunction(args=1, group="Ibama")
def json_leaflet_catalog(values, feature, parent):
  """
  <h4>Return</h4>Leafleft Javascript code
  <p><h4>Syntax</h4>json_leaflet_catalog('satellite')</p>
  <p><h4>Argument</h4>satellite -> name of satellite</p>
  <p><h4>Example</h4>json_leaflet_catalog('landsat')-> { 'name': ..., 'url':.., 'southWest':..., 'northEast':...}</p>
  """
  satellite = values[0]
  crsLayer = qgis.utils.iface.activeLayer().crs()
  geom = feature.geometry()

  cr4326 = QgsCoordinateReferenceSystem( 4326, QgsCoordinateReferenceSystem.EpsgCrsId )
  ct = QgsCoordinateTransform( crsLayer, cr4326 )
  bb = ct.transform( geom.boundingBox() )
  
  image = feature.attribute( 'image' )
  url = "../../tms/%s/%s.tms/{z}/{x}/{y}.png" % ( satellite, image.replace( ".tif", "" ) )
  southWest = "L.latLng( %f, %f )" % ( bb.yMinimum(), bb.xMinimum() )
  northEast = "L.latLng( %f, %f )" % ( bb.yMaximum(), bb.xMaximum() )

  return "{ 'name': '%s', 'url': '%s', 'southWest': %s, 'northEast': %s }" % ( image, url, southWest, northEast)

@qgsfunction(args=1, group="Ibama")
def area_srid(values, feature, parent):
  """
  <h4>Return</h4>Area using the SRID
  <p><h4>Syntax</h4>area_srid(srid)</p>
  <p><h4>Argument</h4>srid -> SRID</p>
  <p><h4>Example</h4>area_srid(5641)-> area</p>
  """
  srid = values[0]
  if not type(srid) is int:
        raise Exception("Enter with SRID(type is integer")
        return -1
  
  crDest = QgsCoordinateReferenceSystem( srid, QgsCoordinateReferenceSystem. InternalCrsId)
  ct = QgsCoordinateTransform( qgis.utils.iface.activeLayer().crs(), crDest )
  geom = QgsGeometry( feature.geometry() )
  geom.transform( ct )
  return geom.area()

@qgsfunction(args=1, group="Ibama")
def is_selected(values, feature, parent):
  # Source: http://gis.stackexchange.com/questions/157718/label-only-selected-feature-using-qgis/157769#157769
  layer = qgis.utils.iface.activeLayer()
  return feature.id() in layer.selectedFeaturesIds()
