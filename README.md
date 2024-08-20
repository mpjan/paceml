# Table of Contents

@!todo

## About PaceML (Pace Markup Language)

PaceML is a markup language designed for representing running workouts in a human-readable and machine-parsable format. It allows for the detailed description of complex workouts including intervals, repetitions, and specialized running segments.

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
4. `@notes`: Additional notes or comments about the workout.

The general syntax for metadata is:

```
@type{value}
```

Example:

```
@title{Easy Tuesday Run}
@date{2024-08-15}
@athlete{John Doe}
@notes{Focus on form and on keeping a 180 SPM cadence}
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
@define_zone[AR]{100}{120}{Active Recovery}
```

Guidelines:

1. At least one zone definition is required, but any number of zones can be defined.
2. The `start` value represents the easiest band of the zone, that is, the slowest pace or lowest heart rate. The `end` value represents the hardest band of the zone.

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
2. `[title]` can be used to provide a brief description of the interval.
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

---

@!parei aqui

#### 1.5 Repetitions

Repetitions are enclosed in `@reps[title]{count}` and `@end_reps` tags. The `[title]` is optional.

```
@reps[Main Set]{4}
  @interval[Work]{400m}{ZT}
  @interval[Recovery]{90s}{RA}
@end_reps
```

### 2.7 Calculations

Total distance and time can be calculated using:

```
@total_distance
@total_time
```

### 2.8 Distance and Time Units

PaceML supports specific formats for distance and time units to ensure consistency and clarity in workout descriptions.

#### 2.8.1 Distance Units

Allowed distance units are:
- m (meters)
- km (kilometers)
- mi (miles)
- yd (yards)

Format: A number followed immediately by the unit, without spaces.

Examples:
```
400m
5km
3.1mi
800yd
```

#### 2.8.2 Time Units

Allowed time units are:
- s (seconds)
- min (minutes)
- h (hours)

For durations less than one hour, times can be expressed in minutes and seconds using the format `MM:SS`.

Format: 
- For single unit times: A number followed immediately by the unit, without spaces.
- For MM:SS format: Two digits for minutes, colon, two digits for seconds.

Examples:
```
30s
5min
2h
01:30 (1 minute 30 seconds)
10:00 (10 minutes)
```

#### 2.8.3 Pace Units

Pace should be expressed in time per distance unit.

Format: `MM:SS/km` or `MM:SS/mi`

Examples:
```
4:30/km
7:15/mi
```

## 3. Complete Example

```
@title{Tuesday Interval Session}
@date{2024-08-15}
@athlete{John Doe}

@define_pace{ZR}{5:30/km}{5:50/km}
@define_pace{ZT}{3:40/km}{4:10/km}

@interval[Warm-up]{10min}{ZR}{note=Focus on gradually increasing your pace}

@reps[Main Set]{6}
  @interval[Speed]{400m}{ZT}{note="Push the pace, but maintain form"}
  @interval[Recovery]{90s}{RA}
@end_reps

@interval[Cool-down]{10min}{ZR}{note="Gradually decrease pace, focus on breathing"}

@interval[Flexibility work]{5min}{ZR}{incline=2%, terrain=treadmill, note="Keep cadence high, even at lower speed"}

@total_distance
@total_time
```

## 4. Parsing Rules

1. Each line represents a single workout component unless within a repetition block.
2. Lines starting with `#` are treated as comments and ignored.
3. Metadata lines (starting with `@`) are processed before the workout content.
4. Custom pace definitions must precede their usage in the workout.
5. Repetition blocks (between `@reps` and `@end_reps`) are processed as a single unit, repeating the enclosed intervals.
6. Calculations (`@total_distance` and `@total_time`) are processed after all intervals.
7. When using a defined pace zone in an interval, any pace within the defined range is considered valid.
8. Titles in square brackets `[]` for `@interval` and `@reps` are optional. If present, they should be used to provide a descriptive name for the interval or repetition set when displaying the workout.

## 5. Output

Parsers should be able to generate:
1. A human-readable summary of the workout
2. A structured data format (e.g., JSON) for integration with other systems
3. Calculated total distance and time

## 6. Extensions

Future versions may include:
1. Support for heart rate zones
2. Integration with GPS data
3. Exporting to common fitness app formats
