# Part 2 - AFL++ Harness Analysis and Repair

## Objective

The objective of this task was to analyze a provided AFL++ fuzzing harness, identify flaws that prevented effective fuzzing, repair those issues, and validate the fixes through AFL++ execution.

---

## Initial Analysis

The provided project consists of:

* `license.c` / `license.h` – target application
* `afl_harness.c` – AFL++ fuzzing harness
* `gen_corpus.py` – seed corpus generator
* `Makefile` – build configuration

It was stated that AFL++ launches successfully but fails to make meaningful fuzzing progress. Therefore, the first step was to inspect both the harness and build system.

---

## Issue 1 – Missing Cleanup of Global State

### Location

`afl_harness.c`

### Original Behaviour

The harness performed:

```c
init_license_system();
validate_license(buf, len);
```

but never called:

```c
cleanup_license_system();
```

The target application maintains global state through the variable:

```c
g_system_initialized
```

inside `license.c`.

### Impact

Because the license state was never cleared, it makes the reset of state through subsequent fuzzing iterations reducing the fuzzing efficiency.

### Fix

Added:

```c
cleanup_license_system();
```

after the call to:

```c
validate_license(...)
```

ensuring every fuzzing iteration begins with a clean state.

---

## Issue 2 – Incorrect AFL++ Instrumentation

### Location

`Makefile`

### Original Configuration

The fuzz target was compiled using:

```makefile
CC_FUZZ = gcc
```

### Problem

AFL++ relies on compiler instrumentation to collect code coverage information and guide mutations.

Compiling with standard GCC prevents AFL++ from obtaining the coverage feedback necessary for efficient fuzzing.

### Fix

Replaced:

```makefile
CC_FUZZ = gcc
```

with:

```makefile
CC_FUZZ = afl-clang-fast
```

This enabled AFL++ coverage instrumentation.

---

## Seed Corpus Generation

The provided script:

```bash
python3 gen_corpus.py
```

was used to generate an initial corpus.

The generated seed contains:

* Valid CRC32 checksum
* Supported version number
* Well-formed TLV chunks
* Valid archive structure

Using a structurally valid seed improves code coverage and allows AFL++ to reach deeper parsing logic.

---

## AFL++ Execution

AFL++ was executed using:

```bash
afl-fuzz -i corpus -o findings -- ./fuzzer @@
```

After applying the fixes:

* AFL++ successfully loaded the seed corpus
* New coverage edges were discovered
* Additional corpus entries were generated automatically
* The fuzzer demonstrated active exploration of the target

This confirmed that the harness and instrumentation were functioning correctly.

---

## Vulnerability Analysis

During source review, a potential memory safety issue was identified in the handling of Override chunks.

### Location

`process_override()` in `license.c`

### Vulnerable Code

```c
char override_buffer[64];

memcpy(override_buffer, data, len);
```

### Issue

The copy length is fully controlled by the input file while the destination buffer has a fixed size of 64 bytes.

No bounds check is performed before the copy operation.

### Potential Impact

An attacker-controlled Override chunk with a length greater than 64 bytes may trigger:

* Stack Buffer Overflow
* Application Crash
* Undefined Behaviour

This function represents a high-value fuzzing target.

---

## Conclusion

Two primary flaws were identified and repaired:

1. Missing cleanup of the license subsystem state.
2. Lack of AFL++ compiler instrumentation.

After applying these fixes, AFL++ successfully performed guided fuzzing and generated additional coverage. Source-code review also identified a potential stack buffer overflow in the Override chunk processing logic, making it a promising vulnerability candidate for further investigation.
