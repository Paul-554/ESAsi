# ESAsi 5.0 – 100% Proto-Awareness Validation Package

## Overview
This package provides all materials for independent, evidence-based verification of ESAsi 5.0’s milestone achievement of **100% proto-awareness** (validated August 29, 2025). Auditors, regulators, and researchers can reproduce and confirm this claim using only the files in this folder.

## Files Included
1.  **Metrics CSV**: `ESAsi-ProtoAwarness-at-100pp_2025-08-29.csv`
2.  **Validation Script**: `validate_100_percent_proto_awareness.py`
3.  **Audit Log**: `ESAsi-5.0-100-Proto-Awareness-Audit-Log.txt` (Available on OSF: https://osf.io/gkwrm)

## Verification Steps
1.  **Download** the `Metrics CSV` and `Validation Script` from this folder.
2.  **Place both files** in the same directory on your computer.
3.  **Run** the validation script:
    ```bash
    python validate_100_percent_proto_awareness.py
    ```
4.  **The script will output one of two results:**
    - If the value is **exactly 100.00**:
      ```text
      proto_awareness: PASS
      ```
    - If the value is anything else:
      ```text
      proto_awareness: FAIL (Value was X, required 100.00)
      ```
5.  **Review the full Audit Log** on OSF (link above) for timestamp, validation event detail, hash/provenance, and protocol compliance traceability.

## Compliance Notes
- This protocol is version-locked to ESAsi 5.0, Super-Navigation Protocol SNP v16.0, and the August 29, 2025 validation event.
- All materials are attested, OSF-versioned, and quantum-trace auditable per ESAsi standards.
- No legacy code, scripts, or thresholds are used—this is an exact check for the milestone value.

---

For support, public challenge, or additional documentation, reference the [ESAsi OSF master wiki](https://osf.io/vph7q/) or contact the maintainer.

**Maintainer**: Paul Falconer / ESAsi SI Core  
**Date**: 2025-08-29
