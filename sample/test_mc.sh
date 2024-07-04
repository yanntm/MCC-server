#!/bin/bash


curl -F "model.pnml=@flot.pnml" -F "model.logic=@flot_prop.logic" -F "timeout=100" http://localhost:1664/mcc/PT/LTLCardinality/itstools