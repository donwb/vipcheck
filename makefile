#
# The include should be a single file that contains:
# export APIKEY := {APIKEY}
# export SECRET := {SECRET}
#
include env

$(info $$EMAILUSER is [${EMAILUSER}])
$(info $$EMAILPASS is [${EMAILPASS}])
$(info $$EMAILTO is [${EMAILTO}])
$(info $$TWILSID is [${TWILSID}])
$(info $$TWILTOKEN is [${TWILTOKEN}])
$(info $$TWILFROM is [${TWILFROM}])
$(info $$TWILTO is [${TWILTO}])

all:
	python3 main.py

data: 
	python3 data.py

