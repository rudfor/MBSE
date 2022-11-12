# Intent: Enable Makefiles to document themselves.
#
# How: This awk-script will parse out the target rules from a Makefile,
# and present any potential comments above each rule as a help message.
#
# Why: Avoid duplicate state as rules are documented exactly one place,
# namely right next to where they are defined in the code.
#
# Usage example (Makefile snippet):
#     # Print documentation for each target rule in this Makefile.
#     help:
#         @awk -f make-help.awk Makefile


# BEGIN-blocks runs once, rest runs per line
BEGIN {
    FS = ":"  # Split fields by colon
    regex_comment      = "^#"                # Must begin with hash
    regex_name         = "[^.#[:space:]]+"   # Any contiguous characters not {whitespace, hash or period}
    regex_rule         = "^" regex_name ":"  # A GNU Make rule line starts with a name followed by colon
    regex_not_internal = "^[^_]"             # Has no leading underscore
}

$0 ~ regex_comment   { comment[NR] = $0 }  # Store all leading comments
$0 ~ regex_rule      { rule = $1 }         # Is the current line a target rule? If so, store its name

rule ~ regex_not_internal {                # Filter out internal rules with leading underscore
    printf "\n%s:\n", rule

    # Walk up the comments until first comment-gap
    for (i = NR-1; comment[i]; i--);

    # Walk down through comments until the rule
    for (i++; i <= NR-1; i++) {
        comment_without_hash = substr(comment[i], 2)  # strip leading hash character
        printf "    %s\n", comment_without_hash;
    }
}

{rule = ""}  # Done with this make target rule, reset and wait for next
