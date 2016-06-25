class Rule:
    """
    the base class of all rules
    """
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True


class HeadingRule(Rule):
    """
    the title takes one line,
    and it`s less than 70 character,
    and it can`t end with colon
    """
    type = 'heading'

    def condition(self, block):
        return not'\n' in block and len(block) <= 70 and not block[-1] == ':'


class TitleRule(HeadingRule):
    """
    title is the first block of document
    """
    type = 'title'
    first = True

    def condition(self, block):
        if not self.first:
            return False
        self.first = False
        return HeadingRule.condition(self, block)


class ListItemRule(Rule):
    """
    listitem is paragraph which begins with hyphen,
    as a part of formatting,
    we should remove the hyphens
    """
    type = 'listitem'

    def condition(self, block):
        return block[0] == '-'

    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True


class ListRule(ListItemRule):
    """
    the list is between the block which isn`t listitem
    and the following listitems,it ends after the last
    continue listitem.
    """
    type = 'list'
    inside = False

    def condition(self, block):
        return True

    def action(self, block, handler):
        if not self.inside and ListItemRule.condition(self, block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block):
            handler.end(self.type)
            self.inside = False
        return False


class ParagraphRule(Rule):
    """
    the paragraph is just something that other rules doesn`t cover
    """
    type = 'paragraph'

    def condition(self, block):
        return True
