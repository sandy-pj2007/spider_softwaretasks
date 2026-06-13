# Part 1 - Vulnerability Analysis of xarinfo

## Environment

* OS: Ubuntu (WSL)
* Compiler: GCC
* Target Application: xarinfo
* Analysis Method: Manual code review and crafted input testing

## Objective

The objective of this task was to analyze the provided XAR archive parser and find the memory safety vulnerabilities by manual inspection and seed generation.

## Initial Analysis

The XAR archive structure consists of:

* File header
* Metadata section
* Chunk records

Using the parser.h file given, a minimal functioning XAR archive was creted.

## Seed Creation

A custom Python script (`make_xar.py`) was written to generate a minimal valid archive.

The generated archive consisted of valid magic bytes(XAR!),version 1 header, empty metadata and zero chunks.

The parser successfully accepted the generated archive and produced a valid archive summary.

## Vulnerability Discovery

### Vulnerability Type

Heap Buffer Overflow / Out-of-Bounds Read

### Location

`parse_metadata()` in `parser.c`

### Relevant Code

```c
memcpy(
    archive->metadata.creator,
    creator_ptr,
    archive->metadata.creator_length
);
```

### Description

The parser copies `creator_length` bytes into the fixed buffer creater[64] without validating the length of bytes copied.Unlike the comment function where the bounds are corrected, here memcpy() is applied directly without checking the creater_length.

This leads to out-of-bounds error when a crafted archive with arbitrary creater_length exceeding the limits is passed.

## Proof of Concept

The valid seed archive was modified by changing:

* `creator_length = 100`

while the archive size remained only 40 bytes.

The modified archive was then executed against the ASAN-instrumented build.

## Result

AddressSanitizer reported:

* Heap Buffer Overflow
* Out-of-Bounds Read
* Crash inside `parse_metadata()`

The crash occurred during the `memcpy()` operation when the parser attempted to read beyond the allocated file buffer.

## Impact

Potential impacts include:

* Application crash (Denial of Service)
* Out-of-Bounds Memory Read
* Possible Information Disclosure
* Undefined Behaviour

## Conclusion

The parser trusts metadata length values supplied by the archive without sufficient validation. The absence of bounds checking for the `creator` field results in a memory safety vulnerability that can be triggered using a crafted XAR archive.
