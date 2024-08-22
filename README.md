# Table of Contents

@!todo

## About PaceML (Pace Markup Language)

PaceML is a markup language designed for representing running workouts in a human-readable and machine-parsable format. It allows for the detailed description of complex workouts including intervals, repetitions, and specialized running segments.

This is what a basic workout might look like in PaceML:

```
# Define the pace zones
@define_zone[RZ]{6:00/km}{5:30/km}{Regenerative Zone}
@define_zone[TZ]{3:30/km}{3:00/km}{Total Effort Zone}

# The workout itself
@interval{10min}{RZ}
@interval{5km}{TZ}
@interval{10min}{RZ}
```

See the full specification below, and more complete examples in the [Examples](@!todo) section.

## PaceML Specification

### 1. Syntax

#### 1.1 Comments

Comments start with `#` and continue to the end of the line.

```
# This is a comment
```

#### 1.2 Metadata

Metadata provides general information about the workout. It is defined using the `@` symbol followed by the metadata type. Metadata should be placed at the beginning of the PaceML document.

Available metadata types:

1. `@title`: Name or title of the workout.
2. `@date`: Date the workout is scheduled.
3. `@athlete`: Name of the athlete performing the workout.

The general syntax for metadata is:

```
@type{value}
```

You can also add free-form notes to a workout. Write these on their own lines.

Example:

```
@title{Easy Tuesday Run}
@date{2024-08-15}
@athlete{Forrest}

Focus on form and on keeping a 180 SPM cadence # This is a note
```

Guidelines:

1. Metadata is optional.
2. If it is present, it should be placed at the beginning of the document.
3. Each metadata field should be on a separate line.
4. Dates should be in ISO 8601 format (`YYYY-MM-DD`).
5. Metadata fields are case-sensitive.

#### 1.3 Zones

Zones define different running zones based on pace or heart rate.

Zones are defined using:

```
@define_zone[zone_name]{start}{end}{description}
```

Example:

```
@define_zone[AR]{6:00/km}{5:30/km}{Active Recovery}
@define_zone[RZ]{5:30/km}{5:00/km}{Regenerative Zone}
@define_zone[MZ]{5:00/km}{4:30/km}{Maintenance Zone}
@define_zone[MZ-EZ]{4:30/km}{4:00/km}{Maintenance Zone - Endurance Zone}
@define_zone[EZ]{4:00/km}{3:30/km}{Endurance Zone}
@define_zone[TZ]{3:30/km}{3:00/km}{Total Effort Zone}
```

Zones can also be defined using heart rate ranges:

```
@define_zone[AR]{100bpm}{120bpm}{Active Recovery}
```

Zones can be defined in a separate document and referenced in the workout in the following way:

```
@import_zones{path/to/zones}
```

Guidelines:

1. At least one zone definition is required, but any number of zones can be defined.
2. The `start` value represents the easiest band of the zone, that is, the slowest pace or lowest heart rate. The `end` value represents the hardest band of the zone.
3. A zone definition should have the same unit of measurement for both the `start` and `end` values.
4. Zone names should be unique, the exception being if the same zone name is used for a pace and a heart rate zone. E.g., `AR` for Active Recovery in both a pace and heart rate zone.

---

#### 1.4 Intervals

Intervals represent specific segments of a workout with a defined:

- Duration or distance; and
- Zone

Intervals are the core building blocks of a workout and are defined using:

```
@interval[title]{duration_or_distance}{zone_name}{additional_parameters}
```

Examples:

```
@interval[Warm-up jog]{10min}{RZ}
@interval{400m}{TZ}
@interval[Hill climb]{5min}{TZ}{incline=5%, note=Focus on form}
@interval[Cool-down jog]{10min}{RZ}{note=Keep moving}
```

Guidelines:

1. `duration_or_distance` and `zone_name` are required fields.
2. `[title]` is optional, and can be used to provide a brief description of the interval.
3. `additional_parameters` can include specific details about the interval, such as incline, terrain, or notes (see below).

##### 1.4.1 Intervals with Additional Parameters

Intervals can include additional parameters to describe various aspects of the workout beyond just duration/distance and zone.

`additional_parameters` can include one or more key-value pairs, separated by commas. These parameters allow for flexible specification of various workout attributes. The available parameters are:

1. `incline`: The incline percentage for treadmill or hill workouts.
2. `terrain`: The type of terrain (e.g., track, trail, treadmill).
3. `note`: Additional notes or instructions for the interval.

If a parameter value needs to include a comma, the entire value should be enclosed in double quotes. Quotes are not necessary for values without commas.

Examples:

```
@interval[Track Work]{400m}{TZ}{terrain=track, note=Focus on form}
@interval[Treadmill Run]{5min}{RZ}{incline=2%, terrain=treadmill, note="Keep cadence high, breathe deeply"}
@interval[Hill Repeats]{2min}{TZ}{note="50m uphill sprint"}
```

#### 1.5 Repetitions

Repetitions define sets of intervals that are repeated multiple times. A repetition block starts with `@reps[title]{count}`, followed by the intervals to be repeated, indented within the block.

Example:

```
@reps[Main Set]{4}
  @interval[Work]{400m}{TZ}
  @interval[Recovery]{90s}{AR}
```

Guidelines:

1. The intervals within a repetition block should be indented with a consistent number of spaces or tabs. The indentation level should be maintained throughout the block.
2. The `[title]` is optional.

#### 1.6 Calculations

Total distance and time for the workout can be calculated by adding the following tags to the end of the document:

```
@total_distance
@total_time
```

#### 1.7 Units

Distance, time and heart rate zones should be specified using consistent units.

##### 1.7.1 Distance Units

Allowed distance units are:

- m (meters)
- km (kilometers)
- mi (miles)
- yd (yards)

Examples:

```
400m
5km
3.1mi
800yd
```

Guidelines:

1. The unit should be placed immediately after the number, without spaces.
2. Units are lowercase.
3. Decimals are specified as dots (`.`).

##### 1.7.2 Time Units

Allowed time units are:

- s (seconds)
- min (minutes)
- h (hours)

Examples:

```
30s
5min
2h
01:30 (1 minute 30 seconds)
2:30 (2 minutes 30 seconds)
10:00 (10 minutes)
```

Guidelines:

1. For single-unit times, the unit should be placed immediately after the number, without spaces, with the unit in lowercase.
2. For multi-unit times, the format should be `MM:SS` or `M:SS` for single-digit minutes.

##### 1.7.3 Pace Units

Pace should be expressed in time per distance unit, separated by a slash (`/`).

Examples:

```
4:30/km
05:30/km
7:15/mi
```

##### 1.7.4 Heart Rate Units

Heart rate units are specified as beats per minute (bpm).

Examples:

```
120bpm
160bpm
```

Guidelines:

1. The unit should be placed immediately after the number, without spaces.
2. Units are lowercase.

### 2. Examples

#### 2.1 Basic Workout

```
@define_zone[RZ]{6:00/km}{5:30/km}{Regenerative Zone}
@define_zone[TZ]{3:30/km}{3:00/km}{Total Effort Zone}

@interval{10min}{RZ}
@interval{5km}{TZ}
@interval{10min}{RZ}
```

#### 2.2 More Complete Workout

##### 2.2.1 Track Workout

```
@title{Tuesday Interval Session}
@date{2024-08-15}
@athlete{Forrest}

Hard interval session on the track.

@define_zone[AR]{6:00/km}{5:30/km}{Active Recovery}
@define_zone{RZ}{5:30/km}{5:50/km}{Regenerative Zone}
@define_zone{MZ}{4:50/km}{5:10/km}{Maintenance Zone}
@define_zone{TZ}{3:40/km}{4:10/km}{Total Effort Zone}

@interval[Warm-up]{10min}{RZ}{note=Don't start too fast}

@reps[Main Set]{6}
  @interval[Speed]{400m}{TZ}{note="Push the pace, but maintain form. First rep is a build-up and can be slower."}
  @interval[Recovery]{90s}{AR}

@interval[Cool-down]{10min}{RZ}{note="Gradually decrease pace, focus on breathing"}

@total_distance
@total_time
```

#### 2.3 Hill Repeats

```
@title{Hill Repeats}
@date{2024-08-15}
@athlete{John Doe}

Today's workout focuses on hill repeats. Hill repeats are a great way to build strength.

@define_zone[AR]{6:00/km}{5:30/km}{Active Recovery}
@define_zone{RZ}{5:30/km}{5:50/km}{Regenerative Zone}
@define_zone{MZ}{4:50/km}{5:10/km}{Maintenance Zone}
@define_zone{TZ}{3:40/km}{4:10/km}{Total Effort Zone}

@interval[Warm-up]{1km}{RZ}

@reps[Hill Repeats]{6}
  @interval[Hill Climb]{2min}{TZ}{incline=15%, note=Focus on form}
  @interval[Recovery]{90s}{AR}

@interval[Cool-down]{1km}{RZ}

@total_distance
@total_time
```

### 3. Parsing Rules

#### 3.1 General Parsing Flow

##### 3.1.1 Tokenization

The parser should first tokenize the PaceML document by breaking it down into individual elements, such as metadata, zone definitions, intervals, repetitions, calculations, and free-form notes.

Comments should be ignored during parsing.

Blank lines should be skipped.

##### 3.1.2 Order of Parsing

1. **Metadata**:
  - Start by identifying and processing metadata at the beginning of the document. 
  - If any metadata fields are in an incorrect format, an error should be raised.
2. **Zone Definitions**:
  - Process zone definitions next. 
  - All zones referenced later in the document should be defined before their usage.
  - Check for consistency in units across zones.
  - If using `@import_zones`, process this before any local zone definitions.
3. **Intervals and Repetitions**:
  - After zones, intervals should be parsed.
  - Intervals and repetitions should be parsed in the order they appear in the document. 
  - Each interval must reference an existing zone and include a valid duration or distance.
  - All referenced zones should be defined. If a zone is missing, raise an error.
  - Verify that interval units are consistent with the zone definitions.
  - The intervals within repetition blocks should be processed recursively.
4. **Calculations**:
  - Calculate total distance and time after all intervals and repetitions have been processed.
  
---

@!parei aqui

##### Handling Imports:
- If the document includes an `@import_zones` statement, the parser should load and parse the referenced file before processing the rest of the document.
- Implement safeguards against circular imports or excessive nesting of imports.

#### 3.2 Error Handling

##### Syntax Errors:
- If any syntax error is encountered (e.g., missing curly braces, undefined zone), the parser should raise an error with a clear message indicating the nature of the error and its location in the document.
- Consider implementing a system for multiple error reporting, allowing the parser to collect and report multiple errors in a single pass.

##### Missing Metadata:
- If required metadata fields are missing, the parser should either raise an error or provide a warning depending on the importance of the metadata for the workout's execution.
- Implement a system to distinguish between required and optional metadata fields.

##### Zone Definition Errors:
- If a zone is defined with inconsistent units or overlapping ranges, the parser should raise an error. 
- The parser should check for duplicate zone names and handle them appropriately (e.g., raise an error or use the last definition).
- Validate that zone ranges are logical (e.g., start value < end value for pace zones).

##### Interval and Repetition Errors:
- The parser should validate that all intervals are properly defined and that repetition counts make sense. 
- Any inconsistencies or illogical combinations should trigger an error (e.g., negative distances or times, zero repetitions).
- Check for references to undefined zones within intervals.

##### Calculation Errors:
- If there is an issue calculating total distance or time (e.g., due to incompatible units), the parser should raise an error.
- Implement proper handling for potential arithmetic overflow in calculations.

#### 3.3 Additional Considerations

##### Unit Conversion:
- Implement a robust system for handling and converting between different units (e.g., km to miles, minutes to seconds).
- Ensure that all calculations and comparisons are done using a standard internal representation to avoid floating-point errors.

#### Extensibility:
- Design the parser to be easily extensible for future additions to the PaceML specification.
- Implement a plugin system or use a strategy pattern to allow for easy addition of new features or modifications to existing parsing rules.

##### Performance:
- For large PaceML documents, consider implementing streaming parsing techniques to handle the document in chunks rather than loading it entirely into memory.
- Optimize the parsing process for common cases while still correctly handling edge cases.

##### Localization:
- Consider implementing support for different locales, particularly for handling decimal separators in numeric values (e.g., 3.14 vs 3,14).

##### Output Format:
- Define a clear and consistent output format for the parsed PaceML document, possibly using a structured format like JSON or XML for easy consumption by other systems.

### 4. Output

Parsers should be able to generate:

1. A human-readable summary of the workout
2. A structured data format (e.g., JSON) for integration with other systems
3. Calculated total distance and time

### 5. Extensions

Future versions may include:

1. Exporting to common fitness app formats
2. Support for additional workout types (e.g., cycling, swimming)
