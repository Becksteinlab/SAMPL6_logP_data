#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create SAMPL6 logP prediction submission files from a CSV of the master spread sheet at
https://docs.google.com/spreadsheets/d/REMOVED/

Download as CSV and provide as the argument to this script.
"""

import os
import textwrap
import pandas as pd

import download_data as gsheet

SOFTWARE = {
    'AMBER':   textwrap.dedent("""\
    Gromacs 2018.2
    MDPOW 0.7.0-dev
    AmberTools
    ACPYPE 0 (2017)
    """),
    'CHARMM': textwrap.dedent("""\
    Gromacs 2018.2
    MDPOW 0.7.0-dev
    CGENFF 2.2.0
    """),
    'LigParGen':   textwrap.dedent("""\
    Gromacs 2018.2
    MDPOW 0.7.0-dev
    LigParGen 2.1
    """),
    'OPLSAA':   textwrap.dedent("""\
    Gromacs 2018.2
    MDPOW 0.7.0-dev
    mol2ff
    """),
}

METHOD_DESCRIPTION = """\
Alchemical free energy calculations were performed in explicit solvent,
following the protocol described in [1].  We used {octanol}.  Parameters were
generated with {parameter_generation}. Files were prepared for Gromacs 2018.
The alchemical data were analyzed with thermodynamic integration. Errors are
reported as errors of the mean (see [1]). The model uncertainty was estimated
on the basis of an unpublished data set of 92 compounds for which we computed
errors for solvation free energies in water and octanol.

[1] I. M. Kenney, O. Beckstein, and B. I. Iorga. Prediction of
cyclohexane-water distribution coefficients for the SAMPL5 data set using
molecular dynamics simulations with the OPLS-AA force field. J Comput Aided Mol
Des, 30(11):1045–1058, 2016."""

METHODS_PARTS = {
    'octanol': {
        'dry': """"dry" octanol (water content 0 mol %)""",
        'wet': """"wet" octanol (water content 27 mol %)""",
        },
    'parameter_generation': {
        'LigParGen': """
                        the OPLS/CM1A LigParGen server http://zarbi.chem.yale.edu/ligpargen/ for
                        OPLS-AA with the TIP4P water model""",
        'OPLSAA': """
                     the OPLSAA mol2ff software (B.I. Iorga, unpublished; also used in [1]) for
                     OPLS-AA with the TIP4P water model""",
        'AMBER': """Antechamber from AmberTools and ACPYPE for AMBER (GAFF) with the TIP3P water model""",
        'CHARMM': """
                     the PARAMCHEM CGENFF program via the server at https://cgenff.umaryland.edu/
                     for CHARMM/CGenFF with the CHARMM TIP3P water model. Note
                     that the latest version of CGENFF produces lone pairs,
                     which are not yet supported in the conversion scripts from
                     CHARMM to Gromacs and a prediction of 0+/-10 is provided for
                     these cases.""",
        },

    }


def collect_data(df, forcefield, dry=True):
    """Extract data for <forcefield> and dry or wet octanol.

    Parameters
    ----------
    df : DataFrame
    forcefield: str
         same as in forcefield column
    dry : bool
         True: dry, False: wet octanol

    Returns
    -------
    method_name, software, data
         method_name is string 'MD-<ff>-<dry|wet>,
         software is string from :data:`SOFTWARE` for the ff,
         data is the dataframe for the Prediction section
    """

    logP, errlogP = ('logPwod', 'errlogPwod') if dry else ('logPwow', 'errlogPwow')
    columns = ["ID", logP, errlogP, "model_uncertainty"]
    type_oct = "dry" if dry else "wet"
    method_name = "MD-{0}-{1}".format(forcefield, "{}oct".format(type_oct))
    software = SOFTWARE[forcefield]
    method_parts = {
        'octanol': METHODS_PARTS['octanol'][type_oct],
        'parameter_generation': textwrap.dedent(
            METHODS_PARTS['parameter_generation'][forcefield]),
        }
    method = METHOD_DESCRIPTION.format(**method_parts)
    return method_name, software, method, df[df.forcefield == forcefield][columns]


def format_sampl6_submission(df, method_name,  software_description, method_description):
    """Return string formatted as submission file for SAMPL6 logP"""

    # header

    buf = textwrap.dedent("""\
    # PARTITION COEFFICIENT PREDICTIONS
    #
    """)

    # prediction section

    buf += textwrap.dedent("""
    # PREDICTION SECTION
    #
    # # Molecule ID, logP, logP SEM, logP model uncertainty
    Predictions:
    """)
    # note: submissions need to have 2 decimals
    buf += df.to_csv(index=False, header=False, float_format="%.2f")


    # name section

    buf += textwrap.dedent("""
    # NAME SECTION
    #
    # Please provide an informal yet informative name of the method used.
    Name:
    {}
    """).format(method_name)

    # software section
    buf += textwrap.dedent("""
    # SOFTWARE SECTION
    #
    # All major software packages used and their versions.
    Software:
    """)
    buf += str(software_description)

    # method category
    buf += textwrap.dedent("""
    # METHOD CATEGORY SECTION
    #
    Category:
    Physical
    """)


    # method description
    buf += textwrap.dedent("""
    # METHOD DESCRIPTION SECTION
    #
    # Methodology and computational details.
    Method:
    """)
    buf += "\n".join(textwrap.wrap(method_description))

    return buf



if __name__ == "__main__":
    import argparse


    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("csvfile", metavar="CSVFILE",
                        help="CSV file of the submission data; will be overwritten if"
                        "--download is set.")
    parser.add_argument("--download", action="store_true",
                        help="Download the latest data from the Google spreadsheet and "
                        "overwrite CSVFILE. Needs the --secret file.")
    parser.add_argument("--modeluncertainty", metavar="FLOAT", type=float, default=1.2,
                        help="estimated error in logP (same for all)")
    parser.add_argument("--ff", metavar="STRING", nargs="+",
                        default=list(SOFTWARE.keys()),
                        help="generate files for these force fields")
    parser.add_argument("--outdir", metavar="DIR", type=str, default=os.curdir,
                        help="Create output files under DIR")
    parser.add_argument("--secret", metavar="JSON", type=str, default="client_secret.json",
                        help="OAuth2 credentials from the Google API Console (service account; "
                        "access to the Google Sheet must must have been shared with the associated "
                        "email address cred.email.")

    args= parser.parse_args()

    if args.download:
        print("Loading data from online Google sheet {}".format(gsheet.SPREADSHEET_ID))
        data = gsheet.get_SAMPL6(secretfile=args.secret)
        data.to_csv(args.csvfile, index=False)
        print("Saved data to {}".format(args.csvfile))
    else:
        print("Loading data from local file {}".format(args.csvfile))
        data = pd.read_csv(args.csvfile)

    data.insert(len(data.columns), 'model_uncertainty', args.modeluncertainty)

    for ff in args.ff:
        for type_oct in True, False:
            method_name, software_descr, method_descr, df = collect_data(data, ff, dry=type_oct)
            outfile = os.path.join(args.outdir,
                                   "logP_prediction-{0}-{1}.csv".format(ff, "octdry" if type_oct else "octwet"))
            buf = format_sampl6_submission(df, method_name, software_descr, method_descr)
            with open(outfile, "w") as out:
                out.write(buf)
            print("Wrote submission file '{}'".format(outfile))
