import ee
import pytest
import os.path
import sys
from geemap import ee_initialize
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from covariateFunctions import prepareCovariates

ee_initialize(token_name= 'EE_SERVICE_ACCOUNT_KEY', auth_mode = 'gcloud', service_account = True)

# Tests that the addcovariates function handles invalid arguments correctly. tags: [edge case]
def test_addCovariates_invalid():
    # Edge case test for adding covariates with invalid arguments
    covariates = ee.Image("LANDSAT/LC08/C01/T1_SR/LC08_044034_20140318")
    proj = 'EPSG:4326'
    nAngles = 10
    prep = prepareCovariates(covariates, proj, nAngles)
    with pytest.raises(TypeError):
        prep.addCovariates(rotatedCoords="True", topoBands="True")

# Tests that the addtopobands function handles an image without elevation data correctly. tags: [edge case]
def test_addTopoBands_noElevation():
    # Edge case test for adding topographic bands to an image without elevation data
    covariates = ee.Image("LANDSAT/LC08/C01/T1_SR/LC08_044034_20140318")
    proj = 'EPSG:4326'
    nAngles = 4
    prep = prepareCovariates(covariates, proj, nAngles)
    with pytest.raises(ee.EEException):
        prep.addTopoBands()

# Tests that the addcovariates function adds topographic bands correctly when rotated coordinates are not added. tags: [happy path]
def test_addCovariates_noRotatedCoords(mocker):
    # Create a mock ee.Image object
    covariates = mocker.Mock(spec=ee.Image)
    # Create an instance of the prepareCovariates class
    prep = prepareCovariates(covariates=covariates, proj='EPSG:4326', nAngles=4)
    # Call the addCovariates function with rotatedCoords set to False
    result = prep.addCovariates(rotatedCoords=False, topoBands=True)
    # Assert that the result has the correct number of bands
    assert result.bandNames().size().getInfo() > 5

# Tests that the addcovariates function adds rotated coordinates correctly when topographic bands are not added. tags: [happy path]
def test_addCovariates_noTopoBands(mocker):
    # Create a mock ee.Image object
    covariates = mocker.Mock(spec=ee.Image)
    # Create an instance of the prepareCovariates class
    prep = prepareCovariates(covariates=covariates, proj='EPSG:4326', nAngles=4)
    # Call the addCovariates function with topoBands set to False
    result = prep.addCovariates(rotatedCoords=True, topoBands=False)
    # Assert that the result has the correct number of bands
    assert result.bandNames().size().getInfo() > 4