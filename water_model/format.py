class Line:
    """each instance of this class represent a new line's content,
    this new line is a combination of several lines from another file.
    """

    def __init__(self, fstline, lncnt):
        """given the line count that this instance should contain.
        also the first line content is given.
        """
        self.lines = [fstline.rstrip('\n')]
        self.lncnt = lncnt

    def feed(self, line):
        if len(self.lines) < self.lncnt:
            self.lines.append(line.rstrip('\n'))

    def content(self):
        '''Returns None if the Line have not stored enough content.'''

        if len(self.lines) < self.lncnt:
            return None
        return ', '.join(self.lines)


def format(incsv, outcsv, lncnt):
    """given the input and output csv file path,
    this function will generate each line of the new file by combining several
    lines into a single line, the number of lines is specified by the paremeter
    -- lncnt.
    """

    lines = []
    with open(incsv) as f:
        for l in f:
            newobj = Line(l, lncnt)
            for oldobj in lines:
                oldobj.feed(l)
            lines.append(newobj)

    with open(outcsv, 'w') as f:
        for obj in lines:
            content = obj.content()
            if content is not None:
                f.write(content + '\n')
