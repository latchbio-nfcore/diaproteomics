from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: str, input_spectral_library: typing.Optional[str], irts: typing.Optional[str], outdir: typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]], email: typing.Optional[str], generate_spectral_library: typing.Optional[bool], input_sheet_dda: typing.Optional[str], skip_decoy_generation: typing.Optional[bool], skip_dia_processing: typing.Optional[bool], generate_pseudo_irts: typing.Optional[bool], irts_from_outer_quantiles: typing.Optional[bool], merge_libraries: typing.Optional[bool], align_libraries: typing.Optional[bool], force_option: typing.Optional[bool], min_upper_edge_dist: typing.Optional[int], pyprophet_global_fdr_level: typing.Optional[str], mztab_export: typing.Optional[bool], library_rt_fdr: typing.Optional[float], min_transitions: typing.Optional[int], max_transitions: typing.Optional[int], decoy_method: typing.Optional[str], unimod: typing.Optional[str], n_irts: typing.Optional[int], min_overlap_for_merging: typing.Optional[int], mz_extraction_window: typing.Optional[int], mz_extraction_window_unit: typing.Optional[str], mz_extraction_window_ms1: typing.Optional[int], mz_extraction_window_ms1_unit: typing.Optional[str], rt_extraction_window: typing.Optional[int], irt_min_rsq: typing.Optional[float], irt_n_bins: typing.Optional[int], irt_min_bins_covered: typing.Optional[int], irt_alignment_method: typing.Optional[str], use_ms1: typing.Optional[bool], cache_option: typing.Optional[str], pyprophet_classifier: typing.Optional[str], pyprophet_fdr_ms_level: typing.Optional[str], pyprophet_peakgroup_fdr: typing.Optional[float], pyprophet_peptide_fdr: typing.Optional[float], pyprophet_protein_fdr: typing.Optional[float], pyprophet_pi0_start: typing.Optional[float], pyprophet_pi0_end: typing.Optional[float], pyprophet_pi0_steps: typing.Optional[float], dialignr_global_align_fdr: typing.Optional[float], dialignr_analyte_fdr: typing.Optional[float], dialignr_unalign_fdr: typing.Optional[float], dialignr_align_fdr: typing.Optional[float], dialignr_query_fdr: typing.Optional[float], dialignr_xicfilter: typing.Optional[str], dialignr_parallelization: typing.Optional[bool], run_msstats: typing.Optional[bool], generate_plots: typing.Optional[bool]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('input_spectral_library', input_spectral_library),
                *get_flag('irts', irts),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('generate_spectral_library', generate_spectral_library),
                *get_flag('input_sheet_dda', input_sheet_dda),
                *get_flag('library_rt_fdr', library_rt_fdr),
                *get_flag('min_transitions', min_transitions),
                *get_flag('max_transitions', max_transitions),
                *get_flag('decoy_method', decoy_method),
                *get_flag('skip_decoy_generation', skip_decoy_generation),
                *get_flag('unimod', unimod),
                *get_flag('skip_dia_processing', skip_dia_processing),
                *get_flag('generate_pseudo_irts', generate_pseudo_irts),
                *get_flag('n_irts', n_irts),
                *get_flag('irts_from_outer_quantiles', irts_from_outer_quantiles),
                *get_flag('merge_libraries', merge_libraries),
                *get_flag('align_libraries', align_libraries),
                *get_flag('min_overlap_for_merging', min_overlap_for_merging),
                *get_flag('mz_extraction_window', mz_extraction_window),
                *get_flag('mz_extraction_window_unit', mz_extraction_window_unit),
                *get_flag('mz_extraction_window_ms1', mz_extraction_window_ms1),
                *get_flag('mz_extraction_window_ms1_unit', mz_extraction_window_ms1_unit),
                *get_flag('rt_extraction_window', rt_extraction_window),
                *get_flag('irt_min_rsq', irt_min_rsq),
                *get_flag('irt_n_bins', irt_n_bins),
                *get_flag('irt_min_bins_covered', irt_min_bins_covered),
                *get_flag('irt_alignment_method', irt_alignment_method),
                *get_flag('force_option', force_option),
                *get_flag('use_ms1', use_ms1),
                *get_flag('min_upper_edge_dist', min_upper_edge_dist),
                *get_flag('cache_option', cache_option),
                *get_flag('pyprophet_classifier', pyprophet_classifier),
                *get_flag('pyprophet_fdr_ms_level', pyprophet_fdr_ms_level),
                *get_flag('pyprophet_global_fdr_level', pyprophet_global_fdr_level),
                *get_flag('pyprophet_peakgroup_fdr', pyprophet_peakgroup_fdr),
                *get_flag('pyprophet_peptide_fdr', pyprophet_peptide_fdr),
                *get_flag('pyprophet_protein_fdr', pyprophet_protein_fdr),
                *get_flag('pyprophet_pi0_start', pyprophet_pi0_start),
                *get_flag('pyprophet_pi0_end', pyprophet_pi0_end),
                *get_flag('pyprophet_pi0_steps', pyprophet_pi0_steps),
                *get_flag('dialignr_global_align_fdr', dialignr_global_align_fdr),
                *get_flag('dialignr_analyte_fdr', dialignr_analyte_fdr),
                *get_flag('dialignr_unalign_fdr', dialignr_unalign_fdr),
                *get_flag('dialignr_align_fdr', dialignr_align_fdr),
                *get_flag('dialignr_query_fdr', dialignr_query_fdr),
                *get_flag('dialignr_xicfilter', dialignr_xicfilter),
                *get_flag('dialignr_parallelization', dialignr_parallelization),
                *get_flag('run_msstats', run_msstats),
                *get_flag('generate_plots', generate_plots),
                *get_flag('mztab_export', mztab_export)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_diaproteomics", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_diaproteomics(input: str, input_spectral_library: typing.Optional[str], irts: typing.Optional[str], outdir: typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]], email: typing.Optional[str], generate_spectral_library: typing.Optional[bool], input_sheet_dda: typing.Optional[str], skip_decoy_generation: typing.Optional[bool], skip_dia_processing: typing.Optional[bool], generate_pseudo_irts: typing.Optional[bool], irts_from_outer_quantiles: typing.Optional[bool], merge_libraries: typing.Optional[bool], align_libraries: typing.Optional[bool], force_option: typing.Optional[bool], min_upper_edge_dist: typing.Optional[int], pyprophet_global_fdr_level: typing.Optional[str], mztab_export: typing.Optional[bool], library_rt_fdr: typing.Optional[float] = 0.01, min_transitions: typing.Optional[int] = 4, max_transitions: typing.Optional[int] = 6, decoy_method: typing.Optional[str] = 'shuffle', unimod: typing.Optional[str] = 'https://raw.githubusercontent.com/nf-core/test-datasets/diaproteomics/unimod.xml', n_irts: typing.Optional[int] = 250, min_overlap_for_merging: typing.Optional[int] = 100, mz_extraction_window: typing.Optional[int] = 30, mz_extraction_window_unit: typing.Optional[str] = 'ppm', mz_extraction_window_ms1: typing.Optional[int] = 10, mz_extraction_window_ms1_unit: typing.Optional[str] = 'ppm', rt_extraction_window: typing.Optional[int] = 600, irt_min_rsq: typing.Optional[float] = 0.95, irt_n_bins: typing.Optional[int] = 10, irt_min_bins_covered: typing.Optional[int] = 8, irt_alignment_method: typing.Optional[str] = 'linear', use_ms1: typing.Optional[bool] = True, cache_option: typing.Optional[str] = 'normal', pyprophet_classifier: typing.Optional[str] = 'LDA', pyprophet_fdr_ms_level: typing.Optional[str] = 'ms1ms2', pyprophet_peakgroup_fdr: typing.Optional[float] = 0.01, pyprophet_peptide_fdr: typing.Optional[float] = 0.01, pyprophet_protein_fdr: typing.Optional[float] = 0.01, pyprophet_pi0_start: typing.Optional[float] = 0.1, pyprophet_pi0_end: typing.Optional[float] = 0.5, pyprophet_pi0_steps: typing.Optional[float] = 0.05, dialignr_global_align_fdr: typing.Optional[float] = 0.01, dialignr_analyte_fdr: typing.Optional[float] = 0.01, dialignr_unalign_fdr: typing.Optional[float] = 0.01, dialignr_align_fdr: typing.Optional[float] = 0.05, dialignr_query_fdr: typing.Optional[float] = 0.05, dialignr_xicfilter: typing.Optional[str] = 'sgolay', dialignr_parallelization: typing.Optional[bool] = True, run_msstats: typing.Optional[bool] = True, generate_plots: typing.Optional[bool] = True) -> None:
    """
    nf-core/diaproteomics

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, input_spectral_library=input_spectral_library, irts=irts, outdir=outdir, email=email, generate_spectral_library=generate_spectral_library, input_sheet_dda=input_sheet_dda, library_rt_fdr=library_rt_fdr, min_transitions=min_transitions, max_transitions=max_transitions, decoy_method=decoy_method, skip_decoy_generation=skip_decoy_generation, unimod=unimod, skip_dia_processing=skip_dia_processing, generate_pseudo_irts=generate_pseudo_irts, n_irts=n_irts, irts_from_outer_quantiles=irts_from_outer_quantiles, merge_libraries=merge_libraries, align_libraries=align_libraries, min_overlap_for_merging=min_overlap_for_merging, mz_extraction_window=mz_extraction_window, mz_extraction_window_unit=mz_extraction_window_unit, mz_extraction_window_ms1=mz_extraction_window_ms1, mz_extraction_window_ms1_unit=mz_extraction_window_ms1_unit, rt_extraction_window=rt_extraction_window, irt_min_rsq=irt_min_rsq, irt_n_bins=irt_n_bins, irt_min_bins_covered=irt_min_bins_covered, irt_alignment_method=irt_alignment_method, force_option=force_option, use_ms1=use_ms1, min_upper_edge_dist=min_upper_edge_dist, cache_option=cache_option, pyprophet_classifier=pyprophet_classifier, pyprophet_fdr_ms_level=pyprophet_fdr_ms_level, pyprophet_global_fdr_level=pyprophet_global_fdr_level, pyprophet_peakgroup_fdr=pyprophet_peakgroup_fdr, pyprophet_peptide_fdr=pyprophet_peptide_fdr, pyprophet_protein_fdr=pyprophet_protein_fdr, pyprophet_pi0_start=pyprophet_pi0_start, pyprophet_pi0_end=pyprophet_pi0_end, pyprophet_pi0_steps=pyprophet_pi0_steps, dialignr_global_align_fdr=dialignr_global_align_fdr, dialignr_analyte_fdr=dialignr_analyte_fdr, dialignr_unalign_fdr=dialignr_unalign_fdr, dialignr_align_fdr=dialignr_align_fdr, dialignr_query_fdr=dialignr_query_fdr, dialignr_xicfilter=dialignr_xicfilter, dialignr_parallelization=dialignr_parallelization, run_msstats=run_msstats, generate_plots=generate_plots, mztab_export=mztab_export)

