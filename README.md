PyZettel
========

# zettel.id.Id

Represents a unique id in a Zettelkasten. Supports both the newer "structure zettel" style of ids that use a
timestamp as well as the older Luhmann-style of ids.

## Usage

- Create an Id: `Id("a")` for Luhmann-style, or `Id("202001020304"")` for a structure zettel style.
- Alternatively: `Id.structure()` to get a structure zettel id for the current time.
- `Id.from_filename("202001020304 name.md")` can be used to get a structure zettel id from a The Archive style of
filename.
- `some_id.next()` will give you the "next" id based on what kind of id is stored. For a Luhmann-style id, it will
parse out the different parts of the id and figure out what the next unique id is. For example:
  `Id("a.1").next() == Id("a.2")`. By default the supported separators are ., -, /, \. It can also figure out that
  a new part of an id has started when the id goes from letters to numbers or vice versa, e.g.:
  `Id("a1").next() == Id("a2")`. If a structure zettel id is used, it parses the string into a `datetime.datetime`
  and uses `datetime.timedelta` to add a minute before converting it back to a string. This ensure that Python is
  handling rolling over all the hours, days, etc. correctly.
- `SEPARATORS` holds the list of supported separator mentione for Luhmann-style zettel ids. Feel free to modify this
if you need to parse ids with your own unique separators that are not accounted for by default.