
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=str,
        default=None,
        section_title='Input/output options',
        description='Input sample sheet (containing path and meta data of raw or mzML files)',
    ),
    'input_spectral_library': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Input sample sheet of spectral libraries (tsv, pqp, TraML)',
    ),
    'irts': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to internal retention time standard sample sheet (tsv, pqp, TraML)',
    ),
    'outdir': NextflowParameter(
        type=typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'generate_spectral_library': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Spectral library generation',
        description='Set this flag if the spectral library should be generated using EasyPQP from provided DDA data - identification search results and corresponding raw data.',
    ),
    'input_sheet_dda': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Input sample sheet to use for library generation eg. DDA raw data (mzML) and DDA identification data (pepXML, mzid, idXML)',
    ),
    'library_rt_fdr': NextflowParameter(
        type=typing.Optional[float],
        default=0.01,
        section_title=None,
        description='PSM fdr threshold to align peptide ids with reference run.',
    ),
    'min_transitions': NextflowParameter(
        type=typing.Optional[int],
        default=4,
        section_title=None,
        description='Minimum number of transitions for assay',
    ),
    'max_transitions': NextflowParameter(
        type=typing.Optional[int],
        default=6,
        section_title=None,
        description='Maximum number of transitions for assay',
    ),
    'decoy_method': NextflowParameter(
        type=typing.Optional[str],
        default='shuffle',
        section_title=None,
        description='Method for generating decoys',
    ),
    'skip_decoy_generation': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Set this flag if using a spectral library that already includes decoy sequences and therefor skip assay and decoy generation.',
    ),
    'unimod': NextflowParameter(
        type=typing.Optional[str],
        default='https://raw.githubusercontent.com/nf-core/test-datasets/diaproteomics/unimod.xml',
        section_title=None,
        description='Path to unimod file needs to be provided',
    ),
    'skip_dia_processing': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Set this flag if you only want to generate spectral libraries from DDA data',
    ),
    'generate_pseudo_irts': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Pseudo iRT generation',
        description='Set this flag if pseudo internal retention time standards should be generated using EasyPQP from provided DDA data - identification search results and corresponding raw data.',
    ),
    'n_irts': NextflowParameter(
        type=typing.Optional[int],
        default=250,
        section_title=None,
        description='Number of pseudo irts selected from dda identifications based on the best q-value',
    ),
    'irts_from_outer_quantiles': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Set this flag if pseudo irts should be selected from the 1st and 4th RT quantile only',
    ),
    'merge_libraries': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Spectral library merging',
        description='Set this flag if the libraries defined in the input or by generation should be merged according to the BatchID',
    ),
    'align_libraries': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Spectral library RT alignment',
        description='Set this flag if pairwise RT alignment should be applied to libraries when merging.',
    ),
    'min_overlap_for_merging': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title=None,
        description='Minimum number of peptides to compute RT alignment during pairwise merging of libraries',
    ),
    'mz_extraction_window': NextflowParameter(
        type=typing.Optional[int],
        default=30,
        section_title='DIA spectral library search',
        description='Mass tolerance for transition extraction (ppm)',
    ),
    'mz_extraction_window_unit': NextflowParameter(
        type=typing.Optional[str],
        default='ppm',
        section_title=None,
        description='Unit for mz window',
    ),
    'mz_extraction_window_ms1': NextflowParameter(
        type=typing.Optional[int],
        default=10,
        section_title=None,
        description='Mass tolerance for precursor transition extraction (ppm)',
    ),
    'mz_extraction_window_ms1_unit': NextflowParameter(
        type=typing.Optional[str],
        default='ppm',
        section_title=None,
        description='Unit for mz window',
    ),
    'rt_extraction_window': NextflowParameter(
        type=typing.Optional[int],
        default=600,
        section_title=None,
        description='RT window for transition extraction (seconds)',
    ),
    'irt_min_rsq': NextflowParameter(
        type=typing.Optional[float],
        default=0.95,
        section_title=None,
        description='Minimal random mean squared error for irt RT alignment',
    ),
    'irt_n_bins': NextflowParameter(
        type=typing.Optional[int],
        default=10,
        section_title=None,
        description='Number of bins defined for the RT Normalization',
    ),
    'irt_min_bins_covered': NextflowParameter(
        type=typing.Optional[int],
        default=8,
        section_title=None,
        description='Number of bins that have to be covered for the RT Normalization',
    ),
    'irt_alignment_method': NextflowParameter(
        type=typing.Optional[str],
        default='linear',
        section_title=None,
        description='Method for irt RT alignment for example',
    ),
    'force_option': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Force the analysis of the OpenSwathWorkflow despite severe warnings',
    ),
    'use_ms1': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Whether to use ms1 information for scoring and extraction',
    ),
    'min_upper_edge_dist': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Minimal distance to the upper edge of a Swath window to still consider a precursor, in Thomson',
    ),
    'cache_option': NextflowParameter(
        type=typing.Optional[str],
        default='normal',
        section_title=None,
        description='Set mode whether to work in memory or to store data as cache first',
    ),
    'pyprophet_classifier': NextflowParameter(
        type=typing.Optional[str],
        default='LDA',
        section_title='False discovery rate estimation',
        description='Machine learning classifier used for pyprophet target / decoy separation',
    ),
    'pyprophet_fdr_ms_level': NextflowParameter(
        type=typing.Optional[str],
        default='ms1ms2',
        section_title=None,
        description='MS Level of pyprophet FDR calculation',
    ),
    'pyprophet_global_fdr_level': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Abstraction level of pyrophet FDR calculation',
    ),
    'pyprophet_peakgroup_fdr': NextflowParameter(
        type=typing.Optional[float],
        default=0.01,
        section_title=None,
        description='Threshold for pyprophet FDR filtering on peakgroup abstraction level',
    ),
    'pyprophet_peptide_fdr': NextflowParameter(
        type=typing.Optional[float],
        default=0.01,
        section_title=None,
        description='Threshold for pyprophet FDR filtering on peptide abstraction level',
    ),
    'pyprophet_protein_fdr': NextflowParameter(
        type=typing.Optional[float],
        default=0.01,
        section_title=None,
        description='Threshold for pyprophet FDR filtering on protein abstraction level',
    ),
    'pyprophet_pi0_start': NextflowParameter(
        type=typing.Optional[float],
        default=0.1,
        section_title=None,
        description='Start for pyprophet non-parametric pi0 estimation',
    ),
    'pyprophet_pi0_end': NextflowParameter(
        type=typing.Optional[float],
        default=0.5,
        section_title=None,
        description='End for pyprophet non-parametric pi0 estimation',
    ),
    'pyprophet_pi0_steps': NextflowParameter(
        type=typing.Optional[float],
        default=0.05,
        section_title=None,
        description='Steps for pyprophet non-parametric pi0 estimation',
    ),
    'dialignr_global_align_fdr': NextflowParameter(
        type=typing.Optional[float],
        default=0.01,
        section_title='MS2 chromatogram alignment',
        description='DIAlignR global alignment FDR threshold: After the chromatogram alignment all peaks should still satisfy the global alignment FDR threshold.',
    ),
    'dialignr_analyte_fdr': NextflowParameter(
        type=typing.Optional[float],
        default=0.01,
        section_title=None,
        description='DIAlignR analyte FDR threshold: Before the chromatogram alignment only peaks satisfying this threshold will be matched across runs.',
    ),
    'dialignr_unalign_fdr': NextflowParameter(
        type=typing.Optional[float],
        default=0.01,
        section_title=None,
        description='DIAlignR unalignment FDR threshold: XICs below this threshold will be considered valid without any alignment.',
    ),
    'dialignr_align_fdr': NextflowParameter(
        type=typing.Optional[float],
        default=0.05,
        section_title=None,
        description='DIAlignR alignment FDR threshold: After the chromatogram alignment aligned peaks should satisfy this threshold.',
    ),
    'dialignr_query_fdr': NextflowParameter(
        type=typing.Optional[float],
        default=0.05,
        section_title=None,
        description='DIAlignR query FDR threshold: During the chromatogram alignment only peaks satisfying this maximum FDR threshold will be considered as potential matches.',
    ),
    'dialignr_xicfilter': NextflowParameter(
        type=typing.Optional[str],
        default='sgolay',
        section_title=None,
        description='DIAlignR XICfilter parameter',
    ),
    'dialignr_parallelization': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Whether DIAlignR should be executed using multithreading (may cause errors)',
    ),
    'run_msstats': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title='Output summary',
        description='Set this flag if statistical normalization and visualizations should be generated using MSstats',
    ),
    'generate_plots': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Set this flag if output plots should be generated.',
    ),
    'mztab_export': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Optional mzTab export (Warning: the mzTab format is not yet well supported for DIA)',
    ),
}

