from __future__ import annotations

SEPARATORS = {'.', '-', '/', '\\'}


class Id:
    def __init__(self, value: str):
        self.value = value
        self.is_scratch = value == SCRATCH_ID_VALUE
        if not self.is_scratch:
            for c in self.value:
                if not c.isalnum() and c not in SEPARATORS:
                    raise ValueError(f"All characters in {value} must be alphanumeric or a known separator.")
        self.parts = self._parse()
        self.has_parent = len(self.parts) > 1

    def next(self):
        if self.is_scratch:
            raise ValueError("Cannot get the next Id of a scratch Id.")
        return Id(self.parts[-1].next())

    def parent(self) -> Id:
        if not self.has_parent:
            raise ValueError(f"Cannot get the parent of root Id {self.value}")
        last = self.parts[-1]
        snd_last = self.parts[-2]
        if snd_last.sep_start > -1:
            return Id(self.value[:snd_last.sep_start])
        return Id(self.value[:last.start])

    def _parse(self) -> list[IdPart]:
        global SEPARATORS

        parts = []
        start = 0
        is_num = self.value[0].isdigit()
        i = 1
        l = len(self.value)
        while i < l:
            c = self.value[i]
            if c in SEPARATORS:
                parts.append(IdPart(self.value, start, i, i, is_num))
                i += 1
                start = i
                ii = 0
                while i + ii < l:
                    cc = self.value[i + ii]
                    if cc in SEPARATORS:
                        ii += 1
                        continue
                    parts[-1].end = i + ii - 1
                    i += ii
                    start = i
                    i += i
                    is_num = cc.isdigit()
                    break
                continue
            if is_num and c.isalpha():
                parts.append(IdPart(self.value, start, i, -1, False))
                start = i
                is_num = False
            elif not is_num and c.isdigit():
                parts.append(IdPart(self.value, start, i, -1, False))
                start = i
                is_num = True
            i += 1
        if start < l:
            parts.append(IdPart(self.value, start, l, -1, is_num))
        return parts

    def compare(self, other: Id):
        parts_l = len(self.parts)
        other_parts_l = len(other.parts)
        smaller_l = min(parts_l, other_parts_l)
        for i in range(smaller_l):
            left = self.parts[i]
            right = other.parts[i]
            r = left.compare(right)
            if r != 0:
                return r
        if parts_l == other_parts_l:
            return 0
        elif parts_l < other_parts_l:
            return -1
        else:
            return 1

    def __eq__(self, other):
        return self.compare(other) == 0

    def __ne__(self, other):
        return self.compare(other) != 0

    def __lt__(self, other):
        return self.compare(other) < 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __gt__(self, other):
        return self.compare(other) > 0

    def __ge__(self, other):
        return self.compare(other) >= 0

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return self.value


class IdPart:
    def __init__(self, value, start, end, sep_start, is_num):
        self.value = value
        self.start = start
        self.end = end
        self.sep_start = sep_start
        self.is_num = is_num
        if is_num:
            self._rollover_char = '9'
        else:
            self._rollover_char = 'Z'

    def id_str(self):
        if self.sep_start == -1:
            return self.value[self.start:self.end]
        else:
            return self.value[self.start:self.sep_start]

    def next(self) -> str:
        last_idx = self._last_idx()
        out: list[str] = [self.value[:self.start]]
        last_rollover_idx = self._find_last_rollover_idx(last_idx)
        if last_rollover_idx == -1:
            self._add_part_with_rollover_last(last_idx, out)
        elif last_rollover_idx == self.start:
            self._add_part_with_rollover_all(last_idx, out)
        else:
            self._add_part_with_partial_rollover(last_idx, last_rollover_idx, out)
        out.append(self.value[last_idx + 1:])
        return ''.join(filter(lambda v: len(v) > 0, out))

    def compare(self, other):
        if self.end < other.end:
            return -1
        if self.end > other.end:
            return 1
        id_s = self.id_str()
        other_id_s = other.id_str()
        min_len = min(len(id_s), len(other_id_s))
        for i in range(min_len):
            c = ord(id_s[i])
            oc = ord(other_id_s[i])
            if self.is_num:
                rank = c - ord('0')
            elif c >= ord('a'):
                rank = c - ord('a')
            else:
                rank = c - ord('A') + 26
            if other.is_num:
                other_rank = oc - ord('0')
            elif oc >= ord('a'):
                other_rank = oc - ord('a')
            else:
                other_rank = oc - ord('A') + 26
            if rank < other_rank:
                return -1
            elif rank > other_rank:
                return 1
        return 0

    def _last_idx(self):
        if self.sep_start < 0:
            return self.end - 1
        return self.sep_start - 1

    def _first_part(self):
        return self.value[:self.start]

    def _last_part(self, last_idx):
        return self.value[last_idx:]

    def _next_char_at(self, i):
        c: int = ord(self.value[i])
        c += 1
        if not self.is_num:
            if c == ord('z') + 1:
                c = ord('A')
        return chr(c)

    def _find_last_rollover_idx(self, last_idx):
        rc = self._rollover_char
        idx = -1
        for i in range(last_idx, self.start - 1, -1):
            c = self.value[i]
            if c == rc:
                idx = i
            else:
                break
        return idx

    def _add_part_with_rollover_last(self, last_idx, out: list[str]):
        out.append(self.value[self.start:last_idx])
        out.append(self._next_char_at(last_idx))

    def _add_part_with_rollover_all(self, last_idx, out: list[str]):
        rolled_over = 'a'
        if self.is_num:
            out.append('0')
            rolled_over = '0'
        else:
            out.append('a')
        out.append(rolled_over * (last_idx - self.start + 1))

    def _add_part_with_partial_rollover(self, last_idx, last_rollover_idx, out: list[str]):
        out.append(self.value[self.start:last_rollover_idx - 1])
        out.append(self._next_char_at(last_rollover_idx - 1))
        rolled_over = 'a'
        if self.is_num:
            rolled_over = '0'
        out.append(rolled_over * (last_idx - last_rollover_idx + 1))

    def __eq__(self, other):
        return self.compare(other) == 0

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.compare(other) > 0

    def __ge__(self, other):
        return self.compare(other) >= 0

    def __lt__(self, other):
        return self.compare(other) < 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __repr__(self):
        return self.id_str()


SCRATCH_ID_VALUE = "**SCRATCH**"
SCRATCH_ID = Id(SCRATCH_ID_VALUE)
