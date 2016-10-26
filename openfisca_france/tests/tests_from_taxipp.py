# -*- coding: utf-8 -*-

import logging
import sys


from openfisca_france.tests.ipp.taxipp_utils import (
    build_openfisca_by_ipp_variables,
    compare, 
    list_dta, 
    run_OF,
    )

log = logging.getLogger(__name__)


def test_from_taxipp(selection = "celib_cadre", threshold = 1, list_input = None, list_output = None,
        verbose = False):
    # selection : dernier mot avant le .dta : "actif-chomeur", "celib_cadre"
    if not list_input:
        list_input, list_output = list_dta(selection)
    elif not list_output:
        list_output = [
            file_path.replace('input', 'output')
            for file_path in list_input
            ]

    openfisca_input_by_ipp_variables, openfisca_output_by_ipp_variables = build_openfisca_by_ipp_variables()
    last_param_scenario = "rien"

    for input_file_path, output_file_path in zip(list_input, list_output):
        log.info("Processing dta files:\n - input file: {}\n - output file: {}".format(
            input_file_path, output_file_path,
            ))
        simulation, param_scenario = run_OF(openfisca_input_by_ipp_variables, path_dta_input = input_file_path,
            option = 'list_dta')
        if str(param_scenario) != str(last_param_scenario):
            pbs = compare(output_file_path, openfisca_output_by_ipp_variables, param_scenario, simulation, threshold,
                verbose = verbose)
            assert len(pbs) == 1, \
                "Avec la base dta {}\n  et un seuil de {} les problèmes suivants ont été identifiés :\n{}".format(
                input_file_path, threshold, pbs)
            last_param_scenario = param_scenario


if __name__ == '__main__':
    import logging
    logging.basicConfig(level = logging.DEBUG, stream = sys.stdout)
    test_from_taxipp(verbose = True)  # list_input = ['base_IPP_input_concubin_10-02-14 16h37.dta'],
