#!/bin/bash


curl -F "model.pnml=@flot.pnml" -F "model.logic=@flot_prop.logic" -F "timeout=100" http://localhost:5000/mcc/PT/LTLCardinality/itstools