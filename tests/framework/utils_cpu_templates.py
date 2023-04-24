# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""Utilities for CPU template related functionality."""

import json
from pathlib import Path

import framework.utils_cpuid as cpuid_utils

# All existing CPU templates available on Intel
INTEL_TEMPLATES = ["C3", "T2", "T2CL", "T2S"]
# All existing CPU templates available on AMD
AMD_TEMPLATES = ["T2A"]
# All existing CPU templates
ALL_TEMPLATES = INTEL_TEMPLATES + AMD_TEMPLATES


def get_supported_cpu_templates():
    """
    Return the list of CPU templates supported by the platform.
    """
    vendor = cpuid_utils.get_cpu_vendor()
    if vendor == cpuid_utils.CpuVendor.INTEL:
        # T2CL template is only supported on Cascade Lake and newer CPUs.
        skylake_model = "Intel(R) Xeon(R) Platinum 8175M CPU @ 2.50GHz"
        if cpuid_utils.get_cpu_model_name() == skylake_model:
            return set(INTEL_TEMPLATES) - set(["T2CL"])
        return INTEL_TEMPLATES
    if vendor == cpuid_utils.CpuVendor.AMD:
        return AMD_TEMPLATES
    return []


SUPPORTED_CPU_TEMPLATES = get_supported_cpu_templates()


def get_supported_custom_cpu_templates():
    """
    Return the list of custom CPU templates supported by the platform.
    """

    def tmpl_name_to_json(name):
        template_path = Path(
            f"../resources/tests/static_cpu_templates/{name.lower()}.json"
        )
        return json.loads(template_path.read_text("utf-8"))

    def name_list_to_tmpl_list(name_list):
        return [tmpl_name_to_json(name) for name in name_list]

    vendor = cpuid_utils.get_cpu_vendor()
    if vendor == cpuid_utils.CpuVendor.INTEL:
        # T2CL template is only supported on Cascade Lake and newer CPUs.
        skylake_model = "Intel(R) Xeon(R) Platinum 8175M CPU @ 2.50GHz"
        if cpuid_utils.get_cpu_model_name() == skylake_model:
            return name_list_to_tmpl_list(set(INTEL_TEMPLATES) - set(["T2CL"]))
        return name_list_to_tmpl_list(INTEL_TEMPLATES)
    if vendor == cpuid_utils.CpuVendor.AMD:
        return name_list_to_tmpl_list(AMD_TEMPLATES)

    return []


SUPPORTED_CUSTOM_CPU_TEMPLATES = get_supported_custom_cpu_templates()