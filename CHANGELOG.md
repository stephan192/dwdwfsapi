## 1.1.0 (2024-03-18)
### Added
- DwdBioWeatherAPI
- DwdPollenFlightAPI

## 1.0.8 (2024-03-08)
### Changed
- Update minimum required Python version to 3.11
- Remove usage of ciso8601
- Update minimum required versions for requests and urllib3
- Remove query for unavailable layer dwd:Warnungen_See
- Add timeout to request.get()

## 1.0.7 (2023-06-03)
### Changed
- Update urllib3 requirement

## 1.0.6 (2022-09-30)
### Changed
- Add option to use a GPS location for the object creation that's used to retrieve the warncell ID

## 1.0.5 (2022-01-23)
### Changed
- Revert changes done in 1.0.4

## 1.0.4 (2021-06-06)
### Changed
- Warncell ID handling due to changes in DWD api

## 1.0.3 (2020-09-26)
### Added
- Urgency attribute added to warning dictionary
### Changed
- Divison criteria between current and expected warnings changed from time to urgency attribute

## 1.0.2 (2020-04-25)
### Added
- Input validation
- Flake8 and pydocstyle conformity

## 1.0.1 (2020-04-20)
### Fixed
- DwdWeatherWarningsAPI: Exception handling when input data is None
- README.md: Typo

## 1.0.0 (2020-04-19)
### Added
- DwdWeatherWarningsAPI